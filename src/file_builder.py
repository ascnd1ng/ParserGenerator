from src import *


def remove_outer_quotes(s):
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    return s


def generate_lr1_class(action_data, goto_data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("class LR1:\n")
        file.write("    def __init__(self):\n")
        file.write("        self.action = {\n")
        for state_ind, actions in action_data.items():
            shifts = []
            reduces = []
            for symbol, act in actions.items():
                symbol = remove_outer_quotes(symbol)
                action_type = act[0]
                if action_type == SHIFT:
                    shifts.append((act[1], symbol))
                elif action_type == REDUCE:
                    if act[2] != (EPS,):
                        out = [remove_outer_quotes(x) for x in act[2]]
                    else:
                        out = f"'{EPS_LETTER}'"
                    reduces.append((act[1], symbol, out))

                elif action_type == ACCEPT:
                    file.write(f"            ({state_ind}, '{symbol}'): '{ACCEPT[0]}',\n")

            shifts.sort(key=lambda x: x[1])
            for next_state, symbol in shifts:
                file.write(f"            ({state_ind}, '{symbol}'): '{SHIFT[0]}{next_state}',\n")

            reduces.sort(key=lambda x: x[1])
            for next_state, symbol, out in reduces:
                file.write(f"            ({state_ind}, '{symbol}'): ['{REDUCE[0]}', '{next_state}', {out}],\n")

        file.write("        }\n\n")

        file.write("        self.goto = {\n")
        for state_ind, gotos in goto_data.items():
            adapted_gotos = []
            for symbol, next_state in gotos.items():
                symbol = f"'{symbol}'"
                adapted_gotos.append((symbol, next_state))
            adapted_gotos.sort(key=lambda x: x[0])
            for symbol, next_state in adapted_gotos:
                file.write(f"            ({state_ind}, {symbol}): {next_state},\n")
        file.write("        }\n")
