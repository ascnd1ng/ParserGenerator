from src import lexer, TopDownParse, Node, Grammar, FirstFollowFinder, Table, Checker


def make_table_generation(pt, i_p, g_p, t_p, patterns, axiom):
    with open(i_p, 'r') as f:
        text = f.read()
    tokens = lexer(text, patterns)
    print(tokens)

    root = TopDownParse(tokens, pt).parse(axiom)
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
    first, follow = fff.find()

    t = Table(nts, ts, rules, first, follow)
    t.compute_table()
    t.gen_file(t_p)
