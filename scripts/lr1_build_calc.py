from generation.gen_lr1_table import LR1
from make_table_generation import lr1_make_table_generation
from src.constants import *

pt = [LR1()]
i_p = '../grammar_descriptions/calculator_grammar.txt'
g_p = '../generation/graph_build_calc.dot'
t_p = '../generation/gen_calc_lr1_table.py'
patterns = patterns_meta
axiom = 'Program'

lr1_make_table_generation(pt, i_p, g_p, t_p, patterns, axiom)
