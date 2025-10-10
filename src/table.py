from .constants import reverse_dict
from pprint import pprint, pformat
import autopep8


class Table:
    def __init__(self, nts, ts, rules, first, follow):
        self.nts = nts
        self.ts = ts
        self.rules = rules
        self.first = first
        self.follow = follow
        self.table = {}
        self.ERROR = 'Error'
        for t in ts:
            for nt in nts:
                self.table[(nt, t)] = self.ERROR
                self.table[(nt, '$')] = self.ERROR

    def ll1check(self, x, a, chain):
        value = self.table[(x, a)]
        if (value != self.ERROR) and (value != chain):
            print(f"Исходная грамматика не LL-1 ({x})")

    def get_chain_first(self, chain):
        res = set()
        for symbol in chain:
            res.update(self.first[symbol])
            if 'eps' not in self.first[symbol]:
                break
        return res

    def purify(self):
        purified_table = {}
        for key in self.table:
            if self.table[key] != self.ERROR:
                purified_table[key] = self.table[key]
        self.table = purified_table

    def compute_table(self):
        for r in self.rules:
            for chain in r.out:
                chain_first = self.get_chain_first(chain)
                x = r.nt
                for a in chain_first:
                    if a != 'eps':
                        self.ll1check(x, a, chain)
                        self.table[(x, a)] = chain
                        if chain[0] != 'eps':
                            self.table[(x, a)] = chain
                        else:
                            self.table[(x, a)] = []

                if 'eps' in chain_first:
                    for b in self.follow[x]:
                        if b != 'eps':
                            self.ll1check(x, b, chain)
                            if chain[0] != 'eps':
                                self.table[(x, b)] = chain
                            else:
                                self.table[(x, b)] = []
        self.purify()

    def reverse_symbol(self, new_symbol):
        if new_symbol in reverse_dict:
            new_symbol = reverse_dict[new_symbol]
        return new_symbol

    def adapt_symbol(self, symbol):
        if symbol[0] != "'":
            new_symbol = "'" + symbol + "'"
        else:
            new_symbol = symbol
        new_symbol = self.reverse_symbol(new_symbol)
        return new_symbol

    def adapt_data(self):
        new_ts = []
        for symbol in self.ts:
            new_symbol = self.adapt_symbol(symbol)
            new_ts.append(new_symbol)
        self.ts = new_ts

        new_nts = []
        for symbol in self.nts:
            new_symbol = self.adapt_symbol(symbol)
            new_nts.append(new_symbol)
        self.nts = new_nts

        new_table = {}
        for key, value in self.table.items():
            new_key = (key[0], self.adapt_symbol(key[1]))
            new_value = []
            for s in value:
                new_value.append(self.adapt_symbol(s))
            new_table[new_key] = new_value

        self.table = new_table

    def gen_t_str(self):
        t_list = ', '.join(self.ts)
        return f"self.t = [{t_list}]"

    def gen_nt_str(self):
        nt_list = ', '.join(self.nts)
        return f"self.nt = [{nt_list}]"

    def gen_table_str(self):
        s = pformat(self.table)
        s = s.replace('"', '')
        return f"self.table = {s}"

    def format_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()

        formatted_code = autopep8.fix_code(original_code, options={'aggressive': 2})

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_code)

    def gen_file(self, file_path):
        self.adapt_data()
        tab = '    '
        t_str = self.gen_t_str()
        nt_str = self.gen_nt_str()
        table_str = self.gen_table_str()
        with open(file_path, 'w') as file:
            file.write("class GeneratedPredictionTable:\n")
            file.write(f"{tab}def __init__(self):\n")
            file.write(f"{tab}{tab}{t_str}\n")
            file.write(f"{tab}{tab}{nt_str}\n")
            file.write(f"{tab}{tab}{table_str}\n")

        self.format_file(file_path)
