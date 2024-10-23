from srcs.backend.game.rules_manager import SUPPORTED_RULES

class settings:
    def __init__(self) -> None:
        self._rule = SUPPORTED_RULES[0]
        self._player1 = "Player_1"
        self._player2 = "Player_2"

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, rule : str):
        if rule not in SUPPORTED_RULES:
            raise Exception(f"rule {rule} not supported!")
        self._rule = rule

    @property
    def player1(self):
        return self._player1

    @player1.setter
    def player1(self, player1 : str):
        if isinstance(player1, str):
            if len(player1) <= 8:
                if player1.isalnum():
                    self._player1 = player1

    @property
    def player2(self):
        return self._player2

    @player2.setter
    def player2(self, player2 : str):
        if isinstance(player2, str):
            if len(player2) <= 8:
                if player2.isalnum():
                    self._player2 = player2
