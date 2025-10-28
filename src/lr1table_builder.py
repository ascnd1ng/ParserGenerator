from collections import defaultdict, deque

from src import END, EPS, Z, SHIFT, REDUCE, ACCEPT


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
        self.first[END] = {END}

    def _index_rules(self):
        index = defaultdict(list)
        for rule in self.rules:
            nt = rule.nt
            out = rule.out
            for i in out:
                index[nt].append(tuple(i))
        return index

    def first_of_sequence(self, sequence):
        result = set()
        if not sequence:
            result.add(EPS)
            return result
        for symbol in sequence:
            result |= (self.first.get(symbol, set()) - {EPS})
            if EPS not in self.first.get(symbol, set()):
                break
        else:
            result.add(EPS)
        return result

    def closure(self, items):
        closure_set = set(items)
        queue = deque(items)

        while queue:
            nt, out, dot_ind, lookahead = queue.popleft()
            if dot_ind < len(out):
                symbol = out[dot_ind]
                if symbol in self.non_terminals:
                    after_dot = out[dot_ind + 1:] + (lookahead,)
                    lookaheads = self.first_of_sequence(after_dot)
                    final_lookaheads = set()
                    for la in lookaheads:
                        if la == EPS:
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

    def goto(self, state, symbol):
        moved = set()
        for nt, out, dot_ind, lookahead in state:
            if dot_ind < len(out) and out[dot_ind] == symbol:
                moved.add((nt, out, dot_ind + 1, lookahead))
        return self.closure(moved) if moved else frozenset()

    def count_states(self):
        start_rule = (Z, (self.axiom,), 0, END)
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
        for state_ind, state in enumerate(self.states):
            self.goto_table[state_ind] = {}
            self.action_table[state_ind] = {}
            for item in state:
                nt = item[0]
                dot_ind = item[2]
                out = item[1]
                lookahead = item[3]

                if (dot_ind < len(out)) and (out != (EPS,)):
                    symbol = out[dot_ind]
                    next_state = self.goto(state, symbol)
                    next_state_ind = self.states.index(next_state)

                    if symbol in self.terminals:
                        self.action_table[state_ind][symbol] = [SHIFT, next_state_ind]
                    else:
                        self.goto_table[state_ind][symbol] = next_state_ind
                else:
                    if nt != 'Z':
                        self.action_table[state_ind][lookahead] = [REDUCE, nt, out]
                    else:
                        self.action_table[state_ind][lookahead] = [ACCEPT, nt, out]
        return self.action_table, self.goto_table
