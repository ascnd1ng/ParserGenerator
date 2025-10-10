from generation.gen_pred_t import GeneratedPredictionTable
from make_table_generation import make_table_generation
from src.constants import *

pt = GeneratedPredictionTable()

i_p = '../grammar_descriptions/calculator_grammar.txt'
g_p = '../generation/graph312.dot'
t_p = '../generation/gen_pred_t_312.py'
patterns = patterns_meta
axiom = 'Program'

make_table_generation(pt, i_p, g_p, t_p, patterns, axiom)
