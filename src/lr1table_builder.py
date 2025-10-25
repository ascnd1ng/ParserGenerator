from collections import defaultdict, deque
from itertools import product


class LR1ParserTableBuilder:
    def __init__(self, terminals, non_terminals, rules, start_symbol, first):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.rules = rules
        self.start_symbol = start_symbol
        self.first = first
        self.rules_index = self._index_rules()
        self.states = []
        self.goto_table = {}
        self.action_table = {}
        if '$' not in self.first:
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
            result |= (self.first[symbol] - {'eps'})
            if 'eps' not in self.first[symbol]:
                break
        else:
            result.add('eps')
        return result

    def closure(self, items):
        closure_set = set(items)
        queue = deque(items)
        while queue:
            lhs, rhs, dot, lookahead = queue.popleft()
            if dot < len(rhs):
                symbol = rhs[dot]
                if symbol in self.non_terminals:
                    beta = rhs[dot + 1:] + (lookahead,)
                    lookaheads = self.first_of_sequence(beta)
                    for prod in self.rules_index[symbol]:
                        for la in lookaheads:
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

    def items(self):
        start_rule = (self.start_symbol + "'", (self.start_symbol,), 0, '$')
        initial = self.closure([start_rule])
        self.states.append(initial)
        queue = deque([initial])
        while queue:
            state = queue.popleft()
            for symbol in self.terminals + self.non_terminals:
                new_state = self.goto(state, symbol)
                if new_state and new_state not in self.states:
                    self.states.append(new_state)
                    queue.append(new_state)
        return self.states

    def build_tables(self):
        self.items()
        for i, state in enumerate(self.states):
            self.action_table[i] = {}
            self.goto_table[i] = {}
            for item in state:
                lhs, rhs, dot, lookahead = item
                if dot < len(rhs):
                    symbol = rhs[dot]
                    goto_state = self.goto(state, symbol)
                    if goto_state:
                        if goto_state not in self.states:
                            self.states.append(goto_state)
                        new_state = self.states.index(goto_state)
                    else:
                        new_state = None
                    if symbol in self.terminals and new_state is not None:
                        self.action_table[i][symbol] = ('shift', new_state)
                    elif symbol in self.non_terminals and new_state is not None:
                        self.goto_table[i][symbol] = new_state
                else:
                    if lhs == self.start_symbol + "'":
                        self.action_table[i]['$'] = ('accept',)
                    else:
                        cur_rule = None
                        for t in self.rules:
                            if t.nt == lhs:
                                cur_rule = t
                        for idx, r in enumerate(cur_rule.out):
                            if r == rhs:
                                rule_no = idx
                                break
                        self.action_table[i][lookahead] = ('reduce', lhs, rhs)
        return self.action_table, self.goto_table
