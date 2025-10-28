from src.lr1table import LR1Axiom, LR1Rules, LR1T, LR1Nt
from make_table_generation import lr1_make_table_generation
from src.constants import *
pt = [LR1Nt(), LR1T(), LR1Rules(), LR1Axiom()]


i_p = '../grammar_descriptions/metagrammar.txt'
g_p = '../generation/gen_table.dot'
t_p = '../generation/gen_lr1_table.py'
patterns = patterns_meta

lr1_make_table_generation([LR1Nt(), LR1T(), LR1Rules(), LR1Axiom()], i_p, g_p, t_p, patterns)
