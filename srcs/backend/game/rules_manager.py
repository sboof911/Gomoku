from srcs.backend.game.rules.standard import standard

SUPPORTED_RULES = ["standard", "PRO", "SWAP"]

class rules:
    def __init__(self, rule = "standard") -> None:
        if rule not in SUPPORTED_RULES:
            raise Exception(f"rule {rule} not supported!")
        self._rule = globals()[rule]()

    def is_legal(self, board, stepx, stepy):
        #SUBJECT RULES
        #.....
        #SPECIFIEDE RULES
        return self._rule.is_legal_move(board, stepx, stepy)
