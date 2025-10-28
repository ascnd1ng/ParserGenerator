from .constants import reverse_dict, reverse_dict_lr1
from pprint import pprint, pformat
import autopep8


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
                if symbol in reverse_dict_lr1:
                    symbol = reverse_dict_lr1[symbol]
                action_type = act[0]
                if action_type == 'shift':
                    shifts.append((act[1], symbol))
                elif action_type == 'reduce':
                    if act[2] != ('eps',):
                        out = [remove_outer_quotes(x) for x in act[2]]
                    else:
                        out = "'ε'"
                    reduces.append((act[1], symbol, out))

                elif action_type == 'accept':
                    file.write(f"            ({state_ind}, {symbol}): 'f',\n")

            shifts.sort(key=lambda x: x[1])
            for next_state, symbol in shifts:
                file.write(f"            ({state_ind}, {symbol}): 's{next_state}',\n")

            reduces.sort(key=lambda x: x[1])
            for next_state, symbol, out in reduces:
                file.write(f"            ({state_ind}, {symbol}): ['r', '{next_state}', {out}],\n")


        file.write("        }\n\n")

        file.write("        self.goto = {\n")
        for state_ind, gotos in goto_data.items():
            for symbol, target in gotos.items():
                symbol = f"'{symbol}'"
                file.write(f"            ({state_ind}, {symbol}): {target},\n")
        file.write("        }\n")
