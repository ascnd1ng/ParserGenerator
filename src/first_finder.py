from src.constants import EPS


class FirstFinder:
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

        first[EPS] = set()
        first[EPS].add(EPS)

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

                        if EPS not in first[c[i]]:
                            add_eps = False
                        i += 1

                    if add_eps:
                        first[rule.nt].add(EPS)

                    if len(first[rule.nt]) != old_len:
                        changed = True

        return first

    def find(self):
        first = self.compute_first()
        return first
