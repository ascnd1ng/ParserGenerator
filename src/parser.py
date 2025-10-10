from collections import deque


class Node:
    num = 0

    def __init__(self, value):
        Node.num += 1
        self.num = Node.num
        self.value = value
        self.attr = None
        self.pos = None
        self.children = []

    def add_child(self, c):
        self.children.append(c)

    def print_graph(self, file):
        label_lines = [str(self.value)]
        if hasattr(self, 'attr') and self.attr:
            label_lines.append(f'attr: {self.attr}')
        if hasattr(self, 'pos') and self.pos:
            label_lines.append(f'pos: {self.pos}')

        formatted_label = '\\n'.join(label_lines)
        file.write(f'{self.num} [label = "{formatted_label}"]\n')

        for c in self.children:
            file.write(f'{self.num} -> {c.num}\n')

        for c in self.children:
            c.print_graph(file)

    def __getitem__(self, i):
        return self.children[i]

    def __len__(self):
        return len(self.children)


class TopDownParse:
    def __init__(self, tokens, PT):
        self.tokens = tokens
        self.PT = PT
        self.magazine = deque()

    def parse(self, axiom):
        root = Node(axiom)
        self.magazine.append(root)
        self.magazine.append(Node('END'))
        token_ind = 0

        while True:
            x = self.magazine[0]
            a = self.tokens[token_ind]
            # print(x.value, a)
            key = (x.value, a[0])
            if x.value == 'END' and 'END' == a[0]:
                break
            if x.value in self.PT.t:
                if x.value == a[0]:
                    x.pos = a[1]
                    x.attr = a[2]
                    self.magazine.popleft()
                    token_ind += 1
                else:
                    raise ValueError(f"Terminal mismatch {x}, {a}")

            elif key in self.PT.table:
                self.magazine.popleft()
                new_nodes = []
                for i in range(len(self.PT.table[key])):
                    new_nodes.append(Node(self.PT.table[key][i]))
                for y in new_nodes:
                    x.add_child(y)
                for y in new_nodes[::-1]:
                    self.magazine.appendleft(y)
            else:
                raise ValueError(f"Non-terminal mismatch {x.value}, {a}")

        return root


class LR1Parse:
    def __init__(self, tokens, action, goto):
        self.tokens = tokens
        self.action = action
        self.goto = goto
        self.magazine = deque()
