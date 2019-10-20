from copy import copy
from collections import defaultdict
from dataclasses import dataclass, asdict
from random import randint


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


def defense_roll(npc: Npc, style: str):
    defense_bonus = asdict(npc.defenses)[style]
    return (npc.defense + 9) * (defense_bonus + 64)


def run(npc: Npc, players):
    players = [player(copy(npc)) for player in players]

    queue = defaultdict(list)
    queue[0] = players

    tick = 0
    while npc.hp > 0:
        yield npc

        if queue[0]:
            # can't react in the middle of a tick
            observed_npc = copy(npc) if tick != 0 else None

            for player in queue[0]:
                delay = player.send(observed_npc)(npc)
                queue[delay].append(player)

        for i in range(max(queue.keys())):
            queue[i] = queue[i + 1]
            del (queue[i + 1])

        tick += 1

    yield npc


def hit(npc: Npc, style: str, attack_roll: int, max_hit: int):
    if roll(npc, style, attack_roll):
        damage = randint(0, max_hit)
        npc.hp -= damage
        return damage
    return 0


def scythe(npc: Npc):
    hit(npc, "slash", 31439, 48 + 24 + 12)
    return 5


def hammer(npc: Npc):
    damage = hit(npc, "crush", 100, 100)
    if damage != 0:
        npc.defense = int(npc.defense * 0.7)
    return 6


def bgs(npc: Npc):
    damage = hit(npc, "slash", 100, 100)
    if damage != 0:
        npc.defense = max(0, int(npc.defense - damage))
    return 7

def roll(npc, style, atkroll):
    defense_roll = npc.defense
    if randint(0, attack_roll) > randint(0, defense_roll):

def clawhit(min_hit, max_hit):
    rolled_hit = random.randint(0, 48)
    return rolled_hit * 1.75

def claws(npc: Npc):
    damage = None

    if roll(npc, "slash", clawatkroll):
        damage = clawhit(44)
    else if roll(npc, "slash", clawatkroll):
        pass
    else if roll(npc, "slash", clawatkroll):
        pass
    else if roll(npc, "slash", clawatkroll):
        pass
    else
        damage = 0

    npc.hp -= damage

    return 4


def doublehammer(npc: Npc):
    yield hammer
    yield hammer

    while True:
        yield scythe


def hammerbgs(npc: Npc):
    yield hammer
    yield bgs

    while True:
        yield scythe


def main():
    for tick, npc in enumerate(
            run(Npc("Tekton", 10000, 100), [hammerbgs, hammerbgs])):
        print("Tick {tick} npc={npc}")

    print("Took {tick-1} ticks")


if __name__ == "__main__":
    main()
