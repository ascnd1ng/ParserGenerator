KW_T = 'KW_T'
KW_NT = 'KW_NT'
KW_AXIOM = 'KW_AXIOM'
KW_EPSILON = 'KW_EPSILON'
TERMINAL = 'term'
IDENT = 'ident'
END = 'END'

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

reverse_dict = {"'terminal'": "'KW_T'",
                "'non-terminal'": "'KW_NT'",
                "'axiom'": "'KW_AXIOM'",
                "'kwepsilon'": "'KW_EPSILON'",
                "'$'": "'END'"
                }
reverse_dict_lr1 = {
    'terminal': "'KW_T'",
    'non-terminal': "'KW_NT'",
    'axiom': "'KW_AXIOM'",
    'kwepsilon': "'KW_EPSILON'",
    '$': "'END'",
    'ident': "'KW_NT'",
    'term': "'KW_T'"
}

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
