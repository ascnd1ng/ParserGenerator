class Checker:
    def __init__(self, nts, ts, rules, axioms, tokens):
        self.nts = nts
        self.ts = ts
        self.rules = rules
        self.axioms = axioms
        self.tokens = tokens

    def find_token(self, name):
        for t in self.tokens:
            if t[2] == name:
                return t

    def check_unused_nt(self):
        all_nts = set(self.nts)
        used_nts = set()

        for r in self.rules:
            rnt = r.nt
            used_nts.add(rnt)

        diff = list(all_nts - used_nts)
        if len(diff) > 0:
            print(f"Неиспользуемый нетерминал: {self.find_token(diff[0])}")

    def is_declared(self, name):
        if (name != 'eps') and (name not in self.nts) and (name not in self.ts):
            return False
        return True

    def check_undeclared_symbols(self):
        for r in self.rules:
            rnt = r.nt
            if rnt not in self.nts:
                print(f"Необъявленный нетерминал: {self.find_token(rnt)}")
            rout = r.out
            for c in rout:
                for s in c:
                    if not self.is_declared(s):
                        print(f"Необъявленный символ: {self.find_token(s)}")

    def check_double_nts_decl(self):
        decl_nts = set()
        for nt in self.nts:
            if nt in decl_nts:
                print(f"Повторное объявление нетерминала: {self.find_token(nt)}")
                return
            else:
                decl_nts.add(nt)

    def check_double_ts_decl(self):

        decl_ts = set()
        for t in self.ts:
            if t in decl_ts:
                print(f"Повторное объявление терминала: {self.find_token(t)}")
                return
            else:
                decl_ts.add(t)

    def check_axioms(self):
        if len(self.axioms) != 1:
            return Exception('Аксиома должна быть ровно 1')

    def check(self):
        print()
        print('Запуск проверок:')
        self.check_unused_nt()
        self.check_undeclared_symbols()
        self.check_axioms()
        self.check_double_nts_decl()
        self.check_double_ts_decl()
        print('Проверки завершены')
        print()
