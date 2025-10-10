from .constants import *


class PredictionTable:
    def __init__(self):
        self.t = [KW_T, KW_NT, KW_AXIOM, KW_EPSILON, TERMINAL, IDENT, ';', '|', '->', ',']
        self.nt = [Program, NT_Decl, T_Decl, A_Decl, RuleList, Rule, NT_Add, T_Add, RuleResult, Chain]
        self.table = {
            # Program
            (Program, KW_NT): [NT_Decl, T_Decl, RuleList, A_Decl],

            # NT_Decl
            (NT_Decl, KW_NT): [KW_NT, IDENT, NT_Add, ';'],

            # NT_Add
            (NT_Add, ','): [',', IDENT, NT_Add],
            (NT_Add, ';'): [],

            # T_Decl
            (T_Decl, KW_T): [KW_T, TERMINAL, T_Add, ';'],

            # T_Add
            (T_Add, ','): [',', TERMINAL, T_Add],
            (T_Add, ';'): [],

            # A_Decl
            (A_Decl, KW_AXIOM): [KW_AXIOM, IDENT, ';'],

            # RuleList
            (RuleList, IDENT): [Rule, RuleList],
            (RuleList, KW_AXIOM): [],

            # Rule
            (Rule, IDENT): [IDENT, '->', RuleResult, ';'],

            # RuleResult
            (RuleResult, IDENT): [Chain, RuleResultTail],
            (RuleResult, TERMINAL): [Chain, RuleResultTail],
            (RuleResult, KW_EPSILON): [Chain, RuleResultTail],

            (RuleResultTail, '|'): ['|', RuleResult],
            (RuleResultTail, ';'): [],

            # Chain
            (Chain, IDENT): [IDENT, Chain],
            (Chain, TERMINAL): [TERMINAL, Chain],
            (Chain, KW_EPSILON): [KW_EPSILON],
            (Chain, '|'): [],
            (Chain, ';'): [],
        }