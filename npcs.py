from dataclasses import dataclass

@dataclass
class Defenses:
    slash: int = 0
    stab: int = 0
    crush: int = 0
    mage: int = 0
    range: int = 0


@dataclass
class Npc:
    name: str = ""
    hp: int = 0
    defense: int = 0
    defenses: Defenses = Defenses()

Tekton5 = Npc(
    name = "Tekton (5 man)",
    hp = 900,
    defense = 213,
    defenses = Defenses(
        stab=155,
        slash=165,
        crush=105
    )
)
