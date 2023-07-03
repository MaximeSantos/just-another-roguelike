from components.base_component import BaseComponent


class Fighter(BaseComponent):
    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        # _hp cannot be set below 0 and won't go beyond the max_hp attribute
        self._hp = max(0, min(value, self.max_hp))
