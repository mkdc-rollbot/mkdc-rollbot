from random import randint
from parser import RollCommand

async def roll_die(command: RollCommand):
    roll_die = lambda: randint(1, command.dice_type)
    rolls = []
    for _ in range(command.dice_count):
        result = roll_die()
        while result in command.reroll_on:
            result = roll_die()
        rolls.append(result)

    kept_rolls = sorted(rolls)
    if command.keep_highest:
        kept_rolls = kept_rolls[-command.keep_highest:]
    elif command.keep_lowest:
        kept_rolls = kept_rolls[:-command.keep_lowest]

    total = sum(kept_rolls) + command.add
    return {"rolls": rolls,
            "kept_rolls": kept_rolls,
            "total": total}
