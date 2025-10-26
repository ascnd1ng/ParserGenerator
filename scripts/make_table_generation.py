from src import lexer, TopDownParse, Node, Grammar, FirstFollowFinder, Table, Checker, reverse_dict_lr1
from src.lr1parser import LR1Parser
from src.lr1table import LR1Nt, LR1T, LR1Rules, LR1Axiom
from src.lr1table_builder import LR1ParserTableBuilder


def generate_lr1_class(action_data, goto_data, file_path):
    with open(file_path, 'w') as file:
        file.write("class LR1:\n")
        file.write("    def __init__(self):\n")
        file.write("        self.action = {\n")
        for state, actions in action_data.items():
            for symbol, act in actions.items():
                if symbol in reverse_dict_lr1:
                    symbol = reverse_dict_lr1[symbol]
                if act[0] == 'shift':
                    file.write(f"            ({state}, {symbol}): 's{act[1]}',\n")
                elif act[0] == 'reduce':
                    rhs = list(act[2]) if isinstance(act[2], tuple) else act[2]
                    file.write(f"            ({state}, {symbol}): ['r', '{act[1]}', {rhs}],\n")
                elif act[0] == 'accept':
                    file.write(f"            ({state}, {symbol}): 'f',\n")
        file.write("        }\n\n")

        file.write("        self.goto = {\n")
        for state, gotos in goto_data.items():
            for symbol, target in gotos.items():
                symbol = f"{symbol}"
                file.write(f"            ({state}, {symbol}): {target},\n")
        file.write("        }\n")


def lr1_make_table_generation(pt, i_p, g_p, t_p, patterns, axiom):
    with open(i_p, 'r') as f:
        text = f.read()
    tokens = lexer(text, patterns)
    print(tokens)

    # root = TopDownParse(tokens, pt).parse(axiom)
    lr1parser = LR1Parser(tokens, pt)
    root = lr1parser.parse_all()
    with open(g_p, 'w') as f:
        f.write('digraph {\n')
        root.print_graph(f)
        f.write('}')

    if t_p is None:
        return root

    g = Grammar()
    g.extract(root)
    nts, ts, rules, axioms = g.get()
    print(g)

    checker = Checker(nts, ts, rules, axioms, tokens)
    checker.check()

    fff = FirstFollowFinder(nts, ts, rules, axioms)
    first, _ = fff.find()

    t_b = LR1ParserTableBuilder(ts, nts, rules, axioms[0], first)
    a_t, g_t = t_b.build_tables()
    print(a_t)
    print(g_t)

    generate_lr1_class(a_t, g_t, t_p)
