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
        if self.attr:
            label_lines.append(f'attr: {self.attr}')
        if self.pos:
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
