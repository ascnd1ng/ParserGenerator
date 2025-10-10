class FirstFollowFinder:
    def __init__(self, nts, ts, rules, axioms):
        self.nts = nts
        self.ts = ts
        self.rules = rules
        self.axioms = axioms

    def compute_first(self):
        first = {}
        for t in self.ts:
            first[t] = set()
            first[t].add(t)
        for nt in self.nts:
            first[nt] = set()

        first['eps'] = set()
        first['eps'].add('eps')

        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                old_len = len(first[rule.nt])
                for c in rule.out:
                    i = 0
                    add_eps = True
                    while (i < len(c)) and add_eps:
                        first[rule.nt].update(first[c[i]])

                        if 'eps' not in first[c[i]]:
                            add_eps = False
                        i += 1

                    if add_eps:
                        first[rule.nt].add('eps')

                    if len(first[rule.nt]) != old_len:
                        changed = True

        return first

    def compute_follow(self, first):
        follow = {}
        for nt in self.nts:
            follow[nt] = set()

        start_symbol = self.axioms[0]
        follow[start_symbol].add('$')

        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                nt = rule.nt
                for c in rule.out:
                    for i in range(len(c)):
                        current = c[i]
                        if current in self.nts:
                            old_len = len(follow[current])

                            # Добавляем следующий first, пока символы могут быть пустыми
                            j = i + 1
                            while j < len(c):
                                next_symbol = c[j]
                                follow[current].update(first.get(next_symbol, set()) - {'eps'})

                                if 'eps' not in first[next_symbol]:
                                    break
                                j += 1

                            # все символы после текущего могут быть пустыми, добавляем follow[nt]
                            all_eps = True
                            for j in range(i + 1, len(c)):
                                if 'eps' not in first.get(c[j], set()):
                                    all_eps = False
                                    break

                            if all_eps:
                                follow[current].update(follow[nt])

                            if len(follow[current]) != old_len:
                                changed = True

        return follow

    def find(self):
        first = self.compute_first()
        follow = self.compute_follow(first)
        return first, follow
