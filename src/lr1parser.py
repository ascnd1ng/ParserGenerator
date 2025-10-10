from collections import deque

lr1table = {
    (0, 'i'): 's4',

    (1, '+'): 's5',
    (1, '$'): 'f',

    (2, '+'): ['r1', 'E', 'T'],
    (2, '*'): 's6',
    (2, '$'): ['r1', 'E', 'T'],

    (3, '+'): ['r3', 'T', 'F'],
    (3, '*'): ['r3', 'T', 'F'],
    (3, '$'): ['r3', 'T', 'F'],

    (4, '+'): ['r5', 'F', 'i'],
    (4, '*'): ['r5', 'F', 'i'],
    (4, '$'): ['r5', 'F', 'i'],

    (5, 'i'): 's4',

    (6, 'i'): 's4',

    (7, '+'): ['r2', 'E', 'E+T'],
    (7, '*'): 's6',
    (7, '$'): ['r2', 'E', 'E+T'],

    (8, '+'): ['r4', 'T', 'T*F'],
    (8, '*'): ['r4', 'T', 'T*F'],
    (8, '$'): ['r4', 'T', 'T*F']
}

goto = {
    (0, 'E'): 1,
    (0, 'T'): 2,
    (0, 'F'): 3,

    (5, 'T'): 7,
    (5, 'F'): 3,

    (6, 'F'): 8
}


def is_finish(action):
    return action[0] == 'f'


def is_reduce(action):
    return action[0][0] == 'r'


def is_shift(action):
    return action[0] == 's'


def extract_state_name(shift):  #s12
    return int(shift[1:])


def extract_out_len(reduce):  #[r2, X, u]
    out_len = len(reduce[-1])
    return int(out_len)


def extract_NT(reduce):  #[r2, X, u]
    return reduce[1]


class LR1Parse:
    def __init__(self, tokens, action, goto):
        self.tokens = tokens
        self.action = action
        self.goto = goto
        self.magazine = deque()

    def parse(self):
        result = list()
        # self.magazine.append('$')
        self.magazine.append(0)
        token_ind = 0
        a = self.tokens[token_ind]

        while 1:
            s = self.magazine[-1]
            print(self.magazine, end= ', ')
            cur_action = self.action[(s, a)]
            print(cur_action)
            if is_shift(cur_action):
                self.magazine.append(extract_state_name(cur_action))
                token_ind += 1
                a = self.tokens[token_ind]
            elif is_reduce(cur_action):
                out_len = extract_out_len(cur_action)
                X = extract_NT(cur_action)
                for i in range(out_len):
                    self.magazine.pop()
                s1 = self.magazine[-1]
                self.magazine.append(self.goto[(s1, X)])
                result.append(cur_action)
            elif is_finish(cur_action):
                return result
            else:
                raise ValueError(f"LR(1) parse ERROR")


lr1 = LR1Parse('i+i*i$', lr1table, goto)
res = lr1.parse()
print(res)