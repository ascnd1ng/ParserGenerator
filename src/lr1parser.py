from collections import deque

from src import lexer
from constants import patterns_meta
from src.lr1table import *

lr1table = {
    (0, 'i'): 's4',

    (1, '+'): 's5',
    (1, 'END'): 'f',

    (2, '+'): ['r1', 'E', 'T'],
    (2, '*'): 's6',
    (2, 'END'): ['r1', 'E', 'T'],

    (3, '+'): ['r3', 'T', 'F'],
    (3, '*'): ['r3', 'T', 'F'],
    (3, 'END'): ['r3', 'T', 'F'],

    (4, '+'): ['r5', 'F', 'i'],
    (4, '*'): ['r5', 'F', 'i'],
    (4, 'END'): ['r5', 'F', 'i'],

    (5, 'i'): 's4',

    (6, 'i'): 's4',

    (7, '+'): ['r2', 'E', 'E+T'],
    (7, '*'): 's6',
    (7, 'END'): ['r2', 'E', 'E+T'],

    (8, '+'): ['r4', 'T', 'T*F'],
    (8, '*'): ['r4', 'T', 'T*F'],
    (8, 'END'): ['r4', 'T', 'T*F']
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
    if reduce[-1] == 'ε':
        return 0
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
        # self.magazine.append('END')
        self.magazine.append(0)
        token_ind = 0
        a = self.tokens[token_ind]

        while 1:
            s = self.magazine[-1]
            print(self.magazine, end=', ')
            cur_action = self.action[(s, a[0])]
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


def lr1parse(text, tokens, LR1):
    lr1 = LR1Parse(tokens, LR1().action, LR1().goto)
    res = lr1.parse()
    print(res)


text = 'axiom Program;'
tokens = lexer(text, patterns_meta)
LR1 = LR1Axiom
lr1parse(text, tokens, LR1)

text = 'non-terminal Program, NT_Decl, NT_Add, T_Decl, T_Add, A_Decl, RuleList, Rule, RuleResult, RuleResultTail, Chain;'
tokens = lexer(text, patterns_meta)
LR1 = LR1Nt
lr1parse(text, tokens, LR1)

text = "terminal '->', ';', '|', ',', 'non-terminal', 'terminal', 'axiom', ident, term, kwepsilon;"
tokens = lexer(text, patterns_meta)
LR1 = LR1T
lr1parse(text, tokens, LR1)

text = """RuleList -> Rule RuleList;
RuleList -> eps;
Rule -> ident '->' RuleResult ';';
RuleResult -> Chain RuleResultTail;
RuleResultTail -> '|' RuleResult | eps;
Chain -> ident Chain;
Chain -> term Chain;
Chain -> kwepsilon;
Chain -> eps;"""
tokens = lexer(text, patterns_meta)
LR1 = LR1Rules
lr1parse(text, tokens, LR1)



# Заготовка построения дерева

# class Node:
#     def __init__(self, value, children=None):
#         self.value = value
#         self.children = children or []  # только названия детей
#
#     def __repr__(self):
#         return f"{self.value}: {self.children}"


# rules = [['r5', 'F', 'i'], ['r3', 'T', 'F'], ['r1', 'E', 'T'],
#          ['r5', 'F', 'i'], ['r3', 'T', 'F'], ['r5', 'F', 'i'],
#          ['r4', 'T', 'T*F'], ['r2', 'E', 'E+T']]
#
# stack = []
#
# for rule in rules:
#     _, lhs, rhs = rule
#     rhs_symbols = list(rhs)
#     children = []
#
#     for symbol in rhs_symbols[::-1]:
#         if stack:
#             child_node = stack.pop()
#             children.insert(0, child_node.value)
#         else:
#             children.insert(0, symbol)
#
#     stack.append(Node(lhs, children))
#
# tree_root = stack[0]
# print(tree_root)
