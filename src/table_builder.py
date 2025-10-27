from .constants import reverse_dict, reverse_dict_lr1
from pprint import pprint, pformat
import autopep8


def generate_lr1_class(action_data, goto_data, file_path):
    with open(file_path, 'w') as file:
        file.write("class LR1:\n")
        file.write("    def __init__(self):\n")
        file.write("        self.action = {\n")
        for state, actions in action_data.items():
            for symbol, act in actions.items():
                if symbol in reverse_dict_lr1:
                    symbol = reverse_dict_lr1[symbol]
                if act[0] == 'shift':
                    file.write(f"            ({state}, {symbol}): 's{act[1]}',\n")
                elif act[0] == 'reduce':
                    rhs = list(act[2]) if isinstance(act[2], tuple) else act[2]
                    file.write(f"            ({state}, {symbol}): ['r', '{act[1]}', {rhs}],\n")
                elif act[0] == 'accept':
                    file.write(f"            ({state}, {symbol}): 'f',\n")
        file.write("        }\n\n")

        file.write("        self.goto = {\n")
        for state, gotos in goto_data.items():
            for symbol, target in gotos.items():
                symbol = f"'{symbol}'"
                file.write(f"            ({state}, {symbol}): {target},\n")
        file.write("        }\n")