from pprint import pprint

from src import lexer, TopDownParse, Node, Grammar, FirstFollowFinder, Checker, reverse_dict_lr1
from src.lr1parser import LR1Parser
from src.lr1table import LR1Nt, LR1T, LR1Rules, LR1Axiom
from src.lr1table_builder import LR1ParserTableBuilder
from src.table_builder import generate_lr1_class


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

    nt_rules = [rules[1], rules[2]]
    print(*nt_rules, sep="\n")
    t_b = LR1ParserTableBuilder(ts, nts, nt_rules,'NT_Decl', first)
    states = t_b.count_states()
    pprint(states)

    a_t, g_t = t_b.build_tables()
    print(a_t)
    print(g_t)

    generate_lr1_class(a_t, g_t, t_p)
