from random import randint
from dice_roller.parser import RollCommand

def roll_die(command: RollCommand):
    roll_die = lambda: randint(1, command.dice_type)
    rolls = []
    for _ in range(command.count):
        result = roll_die()
        while result in command.reroll_list:
            result = roll_die()
        rolls.append(result)

    kept_rolls = sorted(rolls)
    if command.keep_highest:
        kept_rolls = kept_rolls[-command.keep_highest:]
    elif command.keep_lowest:
        kept_rolls = kept_rolls[:-command.keep_lowest]

    total = sum(kept_rolls) + command.add
    return rolls, kept_rolls, total
