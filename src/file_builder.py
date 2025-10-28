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
            for symbol, act in actions.items():
                if symbol in reverse_dict_lr1:
                    symbol = reverse_dict_lr1[symbol]
                action_type = act[0]
                if action_type == 'shift':
                    file.write(f"            ({state_ind}, {symbol}): 's{act[1]}',\n")
                elif action_type == 'reduce':
                    if act[2] != ('eps',):
                        out = [remove_outer_quotes(x) for x in act[2]]
                    else:
                        out = "'ε'"
                    file.write(f"            ({state_ind}, {symbol}): ['r', '{act[1]}', {out}],\n")
                elif action_type == 'accept':
                    file.write(f"            ({state_ind}, {symbol}): 'f',\n")
        file.write("        }\n\n")

        file.write("        self.goto = {\n")
        for state_ind, gotos in goto_data.items():
            for symbol, target in gotos.items():
                symbol = f"'{symbol}'"
                file.write(f"            ({state_ind}, {symbol}): {target},\n")
        file.write("        }\n")
