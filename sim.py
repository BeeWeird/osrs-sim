from copy import copy
from collections import defaultdict
from dataclasses import asdict
from random import randint

from npcs import Npc, Tekton5


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


def ticks_to_kill(npc, players):
    i = -2
    for x in run(copy(npc), players):
        i += 1
    return i


def hit(npc: Npc, style: str, attack_roll: int, max_hit: int):
    if roll(npc, style, attack_roll):
        damage = randint(0, max_hit)
        npc.hp -= damage
        return damage
    return 0


def rapier(npc: Npc):
    hit(npc, "stab", 33525, 53)
    return 4


def dsword(npc: Npc):
    hit(npc, "stab", 29204, 47)
    return 4


def scythe(npc: Npc):
    if roll(npc, "slash", 31439):
        first_roll = randint(0, 48)
        second_roll = randint(0, 24)
        third_roll = randint(0, 12)
        npc.hp -= first_roll + second_roll + third_roll

    return 5


def hammer(npc: Npc):
    damage = hit(npc, "crush", 34736, 73)
    if damage != 0:
        npc.defense = int(npc.defense * 0.7)
    else:
        npc.defense = int(npc.defense * 0.95)
    return 6


def bgs(npc: Npc):
    damage = hit(npc, "slash", 69434, 74)
    if damage != 0:
        npc.defense = max(0, int(npc.defense - damage))
    else:
        npc.defense = max(0, int(npc.defense - 5))
    return 6

def roll(npc, style, attack_roll):
    return randint(0, attack_roll) > randint(0, defense_roll(npc, style))

def clawhit(min_hit, max_hit):
    rolled_hit = randint(0, 48)
    return rolled_hit * 1.75

def claws(npc: Npc):
    damage = None

    if roll(npc, "slash", clawatkroll):
        damage = clawhit(44)
    elif roll(npc, "slash", clawatkroll):
        pass
    elif roll(npc, "slash", clawatkroll):
        pass
    elif roll(npc, "slash", clawatkroll):
        pass
    else:
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
    for tick, npc in enumerate(run(Tekton5, [hammerbgs, hammerbgs])):
        print(f"Tick {tick} npc={npc}")

    print(f"Took {tick-1} ticks")


if __name__ == "__main__":
    main()
