from .constants import *


class Rule:
    def __init__(self, nt, out):
        self.nt = nt
        self.out = out

    def __repr__(self):
        return f"{self.nt} -> {' | '.join(' '.join(inner_list) for inner_list in self.out)}"


class Grammar:
    def __init__(self):
        self.nts = []
        self.ts = []
        self.rules = []
        self.axioms = []

    def get_rule_out(self, root):
        ans = []
        if (root.value == Chain or root.value == RuleResultTail) and (len(root) > 0):
            ans = ans + [root[0].attr]

        for c in root.children:
            ans = ans + self.get_rule_out(c)

        return ans

    def get_rule_alts(self, out):
        res = []
        cur_chain = []
        for c in out:
            if c == '|':
                res.append(cur_chain)
                cur_chain = []
            else:
                cur_chain.append(c)
        res.append(cur_chain)
        return res

    def extract_rule(self, rule_nodes):
        nt = rule_nodes[0].attr
        out = self.get_rule_out(rule_nodes[2])
        out = self.get_rule_alts(out)
        rule = Rule(nt, out)
        return rule

    def extract(self, root):
        if len(root) < 2:
            return

        if root[1].value == '->':
            self.rules.append(self.extract_rule(root.children))
            return

        elif root[0].value == KW_AXIOM:
            self.axioms.append(root[1].attr)

        elif root.value == T_Decl or root.value == T_Add:
            self.ts.append(root[1].attr)

        elif root.value == NT_Decl or root.value == NT_Add:
            self.nts.append(root[1].attr)

        for c in root.children:
            self.extract(c)

    def get(self):
        return self.nts, self.ts, self.rules, self.axioms

    def __str__(self):
        parts = [
            f"Terminals: {self.ts}",
            f"Non-terminals: {self.nts}",
            f"Rules:{chr(10)} {chr(10).join(map(str, self.rules))}",
            f"Axioms: {self.axioms}"
        ]
        return "\n".join(parts)
