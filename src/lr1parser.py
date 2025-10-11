from collections import deque

from src import lexer
from constants import patterns_meta
from src.lr1table import *
from src import Node



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
        self.tree_stack = deque()

    def parse(self):
        # result = list()
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
                # result.append(cur_action)

                children = [self.tree_stack.pop() for _ in range(out_len)][::-1]
                new_node = Node(X)
                for c in children:
                    new_node.add_child(c)
                self.tree_stack.append(new_node)

            elif is_finish(cur_action):
                root = self.tree_stack.pop()
                return root
            else:
                raise ValueError(f"LR(1) parse ERROR")


def lr1parse(text, tokens, LR1):
    lr1 = LR1Parse(tokens, LR1().action, LR1().goto)
    root = lr1.parse()
    with open("lr1_test.dot", 'w') as f:
        f.write('digraph {\n')
        root.print_graph(f)
        f.write('}')


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

text = """Program -> NT_Decl T_Decl RuleList A_Decl;
NT_Decl -> 'non-terminal' ident NT_Add ';';
NT_Add -> ',' ident NT_Add | eps;
T_Decl -> 'terminal' term T_Add ';';
T_Add -> ',' term T_Add | eps;
A_Decl -> 'axiom' ident ';';

RuleList -> Rule RuleList;
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
