import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'generation'))

from prediction_table import PredictionTable
from make_table_generation import make_table_generation
from constants import *
pt = PredictionTable


i_p = '../grammar_descriptions/metagrammar.txt'
g_p = '../generation/graph.dot'
t_p = '../generation/gen_pred_t.py'
patterns = patterns_meta
axiom = 'Program'

make_table_generation(pt, i_p, g_p, t_p, patterns, axiom)
