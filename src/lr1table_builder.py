from .constants import reverse_dict
from pprint import pprint, pformat
import autopep8


class LR1TableBuilder:
    def __init__(self, nts, ts, rules, first, follow):
        self.nts = nts
        self.ts = ts
        self.rules = rules
        self.first = first
        self.table = {}


