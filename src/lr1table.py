from .constants import *


class LR1Axiom:
    def __init__(self):
        self.action = {
            (0, 'axiom'): 's2',
            (1, '$'): 'f',
            (2, 'ident'): 's3',
            (3, ';'): 's4',
            (4, '$'): 'r1'
        }
        self.goto = {
            (0, 'A_Decl'): 1
        }


class LR1Nt:
    def __init__(self):
        self.action = {
            (0, 'non-terminal'): 's2',
            (1, '$'): 'f',
            (2, 'ident'): 's3',
            (3, ';'): 'r3',
            (3, ','): 's5',
            (4, ';'): 's6',
            (5, 'ident'): 's7',
            (6, '$'): 'r1',
            (7, ';'): 'r3',
            (7, ','): 's5',
            (8, ';'): 'r2'
        }
        self.goto = {
            (0, 'NT_Decl'): 1,
            (3, 'NT_Add'): 4,
            (7, 'NT_Add'): 8
        }


class LR1T:
    def __init__(self):
        self.action = {
            (0, 'terminal'): 's2',
            (1, '$'): 'f',
            (2, 'term'): 's3',
            (3, ';'): 'r3',
            (3, ','): 's5',
            (4, ';'): 's6',
            (5, 'term'): 's7',
            (6, '$'): 'r1',
            (7, ';'): 'r3',
            (7, ','): 's5',
            (8, ';'): 'r2'
        }
        self.goto = {
            (0, 'T_Decl'): 1,
            (3, 'T_Add'): 4,
            (7, 'T_Add'): 8
        }


class LR1Rules:
    def __init__(self):
        self.action = {
            (0, 'ident'): 's3',
            (0, '$'): 'r2',
            (1, '$'): 'f',
            (2, 'ident'): 's3',
            (2, '$'): 'r2',
            (3, "'"): 's5',
            (4, '$'): 'r1',
            (5, 'ident'): 'r3',
            (5, '$'): 'r3'
        }

        self.goto = {
            (0, 'RuleList'): 1,
            (0, 'Rule'): 2,
            (2, 'RuleList'): 4,
            (2, 'Rule'): 2
        }
