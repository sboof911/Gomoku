from srcs.backend.game.rules_manager import SUPPORTED_RULES

class settings:
    def __init__(self) -> None:
        self._rule = SUPPORTED_RULES[0]
        self._player1 = "Sboof"
        self._player2 = "Hmida"
        self._AIName = "AI"
        self._debug_mode = False
        self._difficulty_level = 1
        self._backgroud_img = 0

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, rule : str):
        if rule not in SUPPORTED_RULES:
            raise Exception(f"rule {rule} not supported!")
        self._rule = rule

    @property
    def AIName(self):
        return self._AIName

    def can_set_name(self, name : str):
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        if len(name) > 8 or 1 > len(name):
            raise ValueError("name must be less than 8 characters")
        if not name.isalnum():
            raise ValueError("name must be alphanumeric")

    @AIName.setter
    def AIName(self, AIName : str):
        self.can_set_name(AIName)
        self._AIName = AIName

    @property
    def player1(self):
        return self._player1

    @player1.setter
    def player1(self, player1 : str):
        self.can_set_name(player1)
        self._player1 = player1
                    

    @property
    def player2(self):
        return self._player2

    @player2.setter
    def player2(self, player2 : str):
        self.can_set_name(player2)
        self._player2 = player2

    @property
    def debug_mode(self):
        return self._debug_mode

    @debug_mode.setter
    def debug_mode(self, debug_mode : bool):
        if not isinstance(debug_mode, bool):
            raise ValueError("debug_mode must be a boolean")
        self._debug_mode = debug_mode

    @property
    def difficulty_level(self):
        return self._difficulty_level

    @difficulty_level.setter
    def difficulty_level(self, difficulty_level : int):
        if not isinstance(difficulty_level, int):
            raise ValueError("difficulty_level must be an integer")
        if 1 > difficulty_level or difficulty_level > 3:
            raise ValueError("difficulty_level must be between 1 and 3")
        self._difficulty_level = difficulty_level
