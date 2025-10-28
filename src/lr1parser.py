from collections import deque
from src import Node, EPS_LETTER, ACCEPT, REDUCE, SHIFT, PARSER_START_NODE


def is_accept(action):
    return action[0] == ACCEPT[0]


def is_reduce(action):
    return action[0][0] == REDUCE[0]


def is_shift(action):
    return action[0] == SHIFT[0]


def extract_state_name(shift):  #s12
    return int(shift[1:])


def extract_out_len(reduce):  #[r2, X, u]
    if reduce[-1] == EPS_LETTER:
        return 0
    out_len = len(reduce[-1])
    return int(out_len)


def extract_NT(reduce):  #[r2, X, u]
    return reduce[1]


class LR1Parser:
    def __init__(self, tokens, LR1s):
        self.goto = None
        self.action = None
        self.tokens = tokens
        self.LR1s = LR1s
        self.magazine = deque()
        self.tree_stack = deque()

    def parse_all(self):
        token_ind = 0
        roots = []
        for lr1table in self.LR1s:
            self.action = lr1table.action
            self.goto = lr1table.goto
            root, token_ind = self.parse(token_ind)
            roots.append(root)
        if len(roots) > 1:
            root = Node(PARSER_START_NODE)
            for c in roots:
                root.add_child(c)
            return root
        return roots[0]

    def parse(self, token_ind):
        self.magazine.append(0)
        a = self.tokens[token_ind]

        while 1:
            s = self.magazine[-1]
            print(self.magazine, end=', ')
            cur_action = self.action[(s, a[0])]
            print(cur_action)
            if is_shift(cur_action):
                self.magazine.append(extract_state_name(cur_action))

                new_node = Node(a[0])
                new_node.pos = a[1]
                new_node.attr = a[2]
                self.tree_stack.append(new_node)

                token_ind += 1
                a = self.tokens[token_ind]

            elif is_reduce(cur_action):
                out_len = extract_out_len(cur_action)
                X = extract_NT(cur_action)
                for i in range(out_len):
                    self.magazine.pop()
                s1 = self.magazine[-1]
                self.magazine.append(self.goto[(s1, X)])

                children = [self.tree_stack.pop() for _ in range(out_len)][::-1]
                new_node = Node(X)
                for c in children:
                    new_node.add_child(c)
                self.tree_stack.append(new_node)

            elif is_accept(cur_action):
                root = self.tree_stack.pop()
                return root, token_ind
            else:
                raise ValueError(f"LR(1) parse ERROR")
