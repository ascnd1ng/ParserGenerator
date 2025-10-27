from collections import defaultdict, deque


class LR1ParserTableBuilder:
    def __init__(self, terminals, non_terminals, rules, axiom, first):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.rules = rules
        self.axiom = axiom
        self.first = first
        self.rules_index = self._index_rules()
        self.states = []
        self.goto_table = {}
        self.action_table = {}
        self.first['$'] = {'$'}

    def _index_rules(self):
        index = defaultdict(list)
        for x in self.rules:
            lhs = x.nt
            rhs = x.out
            for i in rhs:
                index[lhs].append(tuple(i))
        return index

    def first_of_sequence(self, sequence):
        result = set()
        if not sequence:
            result.add('eps')
            return result
        for symbol in sequence:
            result |= (self.first.get(symbol, set()) - {'eps'})
            if 'eps' not in self.first.get(symbol, set()):
                break
        else:
            result.add('eps')
        return result

    def closure(self, items):
        closure_set = set(items)
        queue = deque(items)

        while queue:
            nt, out, dot, lookahead = queue.popleft()
            if dot < len(out):
                symbol = out[dot]
                if symbol in self.non_terminals:
                    beta = out[dot + 1:] + (lookahead,)
                    lookaheads = self.first_of_sequence(beta) # ТУТ
                    final_lookaheads = set()
                    for la in lookaheads:
                        if la == 'eps':
                            final_lookaheads.add(lookahead)
                        else:
                            final_lookaheads.add(la)
                    for prod in self.rules_index[symbol]:
                        for la in final_lookaheads:
                            item = (symbol, prod, 0, la)
                            if item not in closure_set:
                                closure_set.add(item)
                                queue.append(item)
        return frozenset(closure_set)

    def goto(self, items, symbol):
        moved = set()
        for lhs, rhs, dot, lookahead in items:
            if dot < len(rhs) and rhs[dot] == symbol:
                moved.add((lhs, rhs, dot + 1, lookahead))
        return self.closure(moved) if moved else frozenset()

    def count_states(self):
        start_rule = ('Z', (self.axiom,), 0, '$')
        initial = self.closure([start_rule])
        self.states.append(initial)
        queue = deque([initial])
        symbols = list(self.terminals) + list(self.non_terminals)
        while queue:
            state = queue.popleft()
            for symbol in symbols:
                new_state = self.goto(state, symbol)
                if new_state and new_state not in self.states:
                    self.states.append(new_state)
                    queue.append(new_state)
        return self.states

    def build_tables(self):
