from pprint import pprint
from src import lexer, Grammar, FirstFinder, Checker
from src.lr1parser import LR1Parser
from src.lr1table_builder import LR1ParserTableBuilder
from src.file_builder import generate_lr1_class


def lr1_make_table_generation(pt, i_p, g_p, t_p, patterns):
    with open(i_p, 'r') as f:
        text = f.read()
    tokens = lexer(text, patterns)
    print(tokens)

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

    fff = FirstFinder(nts, ts, rules, axioms)
    first = fff.find()

    t_b = LR1ParserTableBuilder(nts, ts, rules, axioms[0], first)

    states = t_b.count_states()
    pprint(states)

    a_t, g_t = t_b.build_tables()
    print(a_t)
    print(g_t)

    generate_lr1_class(a_t, g_t, t_p)
