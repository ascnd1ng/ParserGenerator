import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'generation'))

from gen_pred_t_312 import GeneratedPredictionTable
from constants import *
from make_table_generation import make_table_generation

i_p = '../grammar_descriptions/arithmetic_expression.txt'
g_p = '../generation/graph312expression.dot'
t_p = None

pt = GeneratedPredictionTable
patterns = patterns_calc
axiom = 'E1'

root = make_table_generation(pt, i_p, g_p, t_p, patterns, axiom)

res = []


def calc(root, res):
    if root.value in ['*', '+', 'n', '(', ')']:
        res.append(root.attr)
        return
    for c in root.children:
        calc(c, res)


calc(root, res)
expr = ''.join(res)


def calculate_expression(s):
    def evaluate(tokens):
        stack = []
        num = 0
        sign = '+'

        while tokens:
            token = tokens.pop(0)

            if token.isdigit():
                num = int(token)

            if token == '(':
                num = evaluate(tokens)

            if not token.isdigit() or not tokens:
                if sign == '+':
                    stack.append(num)
                elif sign == '*':
                    stack.append(stack.pop() * num)

                sign = token
                num = 0

                if token == ')':
                    break

        return sum(stack)

    tokens = []
    i = 0
    while i < len(s):
        if s[i] == ' ':
            i += 1
            continue
        if s[i] in '()+*':
            tokens.append(s[i])
            i += 1
        else:
            num_str = ''
            while i < len(s) and s[i].isdigit():
                num_str += s[i]
                i += 1
            tokens.append(num_str)

    return evaluate(tokens)


result = calculate_expression(expr)
print(result)
