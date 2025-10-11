from .constants import *


class LR1Axiom:
    def __init__(self):
        self.action = {
            (0, KW_AXIOM): 's2',
            (1, END): 'f',
            (2, IDENT): 's3',
            (3, ';'): 's4',
            (4, END): ['r1', A_Decl, [KW_AXIOM, IDENT, ';']]
        }
        self.goto = {
            (0, A_Decl): 1
        }


class LR1Nt:
    def __init__(self):
        self.action = {
            (0, KW_NT): 's2',
            (1, KW_T): 'f',
            (2, IDENT): 's3',
            (3, ';'): ['r3', NT_Add, 'ε'],
            (3, ','): 's5',
            (4, ';'): 's6',
            (5, IDENT): 's7',
            (6, KW_T): ['r1', NT_Decl,  [KW_NT, IDENT, NT_Add, ';']],
            (7, ';'): ['r3', NT_Add, 'ε'],
            (7, ','): 's5',
            (8, ';'): ['r2', NT_Add, [',', IDENT, NT_Add]]
        }
        self.goto = {
            (0, NT_Decl): 1,
            (3, NT_Add): 4,
            (7, NT_Add): 8
        }


class LR1T:
    def __init__(self):
        self.action = {
            (0, KW_T): 's2',
            (1, IDENT): 'f',
            (2, TERMINAL): 's3',
            (3, ';'): ['r3', T_Add, 'ε'],
            (3, ','): 's5',
            (4, ';'): 's6',
            (5, TERMINAL): 's7',
            (6, IDENT): ['r1', T_Decl,  [KW_T, TERMINAL, T_Add, ';']],
            (7, ';'): ['r3', T_Add, 'ε'],
            (7, ','): 's5',
            (8, ';'): ['r2', T_Add, [',', TERMINAL, T_Add]]
        }
        self.goto = {
            (0, T_Decl): 1,
            (3, T_Add): 4,
            (7, T_Add): 8
        }


class LR1Rules:
    def __init__(self):
        self.action = {
            (0, IDENT): 's3',
            (0, KW_AXIOM): ['r2', RuleList,  'ε'],

            (1, KW_AXIOM): 'f',

            (2, IDENT): 's3',
            (2, KW_AXIOM): ['r2', RuleList,  'ε'],

            (3, '->'): 's5',

            (4, KW_AXIOM): ['r1', RuleList, [Rule, RuleList]],

            (5, IDENT): 's8',
            (5, ';'): ['r10', Chain, 'ε'],
            (5, '|'): ['r10', Chain, 'ε'],
            (5, TERMINAL): 's9',
            (5, KW_EPSILON): 's10',

            (6, ';'): 's11',

            (7, ';'): ['r6', RuleResultTail, 'ε'],
            (7, '|'): 's13',

            (8, IDENT): 's8',
            (8, ';'): ['r10', Chain, 'ε'],
            (8, '|'): ['r10', Chain, 'ε'],
            (8, TERMINAL): 's9',
            (8, KW_EPSILON): 's10',

            (9, IDENT): 's8',
            (9, ';'): ['r10', Chain, 'ε'],
            (9, '|'): ['r10', Chain, 'ε'],
            (9, TERMINAL): 's9',
            (9, KW_EPSILON): 's10',

            (10, ';'): ['r9', Chain, [KW_EPSILON]],
            (10, '|'): ['r9', Chain, [KW_EPSILON]],

            (11, IDENT): ['r3', Rule, [IDENT, '->', RuleResult, ';']],
            (11, KW_AXIOM): ['r3', Rule, [IDENT, '->', RuleResult, ';']],

            (12, ';'): ['r4', RuleResult, [Chain, RuleResultTail]],

            (13, IDENT): 's8',
            (13, ';'): ['r10', Chain, 'ε'],
            (13, '|'): ['r10', Chain, 'ε'],
            (13, TERMINAL): 's9',
            (13, KW_EPSILON): 's10',

            (14, ';'): ['r7', Chain, [IDENT, Chain]],
            (14, '|'): ['r7', Chain, [IDENT, Chain]],

            (15, ';'): ['r8', Chain, [TERMINAL, Chain]],
            (15, '|'): ['r8', Chain, [TERMINAL, Chain]],

            (16, ';'): ['r5', RuleResultTail, ['|', RuleResult]]
        }

        self.goto = {
            (0, RuleList): 1,
            (0, Rule): 2,

            (2, RuleList): 4,
            (2, Rule): 2,

            (5, RuleResult): 6,
            (5, Chain): 7,

            (7, RuleResultTail): 12,

            (8, Chain): 14,

            (9, Chain): 15,

            (13, RuleResult): 16,
            (13, Chain): 7,
        }
