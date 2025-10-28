KW_T = 'terminal'
KW_NT = 'non-terminal'
KW_AXIOM = 'axiom'
KW_EPSILON = 'epsilon'
TERMINAL = 'term'
IDENT = 'ident'
END = '$'

Program = 'Program'
Rule = 'Rule'
NT_Decl = 'NT_Decl'
T_Decl = 'T_Decl'
A_Decl = 'A_Decl'
RuleList = 'RuleList'
NT_Add = 'NT_Add'
T_Add = 'T_Add'
RuleResult = 'RuleResult'
RuleResultTail = 'RuleResultTail'
Chain = 'Chain'

patterns_meta = [
    (r'non-terminal', KW_NT),
    (r'terminal', KW_T),
    (r'epsilon', KW_EPSILON),
    (r'axiom', KW_AXIOM),
    (r'[A-Z][0-9A-Za-z_]+', IDENT),
    (r"'[^']*'|[a-z]+", TERMINAL),
    (r'\|', '|'),
    (r'->', '->'),
    (r',', ','),
    (r';', ';')
]

patterns_calc = [
    (r'[0-9]+', 'n'),
    (r'\+', '+'),
    (r'\*', '*'),
    (r'\(', '('),
    (r'\)', ')')
]

SHIFT = 'shift'
REDUCE = 'reduce'
ACCEPT = 'accept'
EPS_LETTER = 'ε'
EPS = 'eps'
Z = 'Z'
