def is_finish(action):
    return action[0] == 'f'


def is_reduce(action):
    return action[0] == 'r'


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
        self.magazine.append('END')
        self.magazine.append('Z')  #fake axiom
        token_ind = 0
        a = self.tokens[token_ind]

        while 1:
            s = self.magazine[-1]
            cur_action = self.action[s, a]
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
                self.magazine.append(self.goto[s1, X])
                result.append(cur_action)
            elif is_finish(cur_action):
                return
            else:
                raise ValueError(f"LR(1) parse ERROR")