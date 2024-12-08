import random
import sys
from collections import Counter

def roll_dice(n):
    return [random.randint(0, 9) for _ in range(n)]

def find_bonus(rolls):
    counts = Counter(rolls)
    most_common = counts.most_common()
    bonus = ""

    for value, count in most_common:
        if count >= 2:
            if count == 2:
                bonus = f"DOUBLE ({value})"
            elif count == 3:
                bonus = f"TRIPLE ({value})"
            elif count == 4:
                bonus = f"QUADRUPLE ({value})"
            elif count == 5:
                bonus = f"QUINTUPLE ({value})"
            elif count == 6:
                bonus = f"SIXTUPLE ({value})"
            elif count == 7:
                bonus = f"SEPTUPLE ({value})"
            elif count == 8:
                bonus = f"OCTUPLE ({value})"
            elif count == 9:
                bonus = f"NONUPLE ({value})"
            elif count == 10:
                bonus = f"DECUPLE ({value})"
            break

    return bonus

def main(n):
    rolls = roll_dice(n)
    letters = "Q R S T U V W X Y Z".split()

    for i in range(n):
        print(f"{letters[i]} = {rolls[i]}")

    bonus = find_bonus(rolls)
    if bonus:
        print(f"BONUS ~ {bonus}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dice-roll.py <number_of_dice>")
        sys.exit(1)

    try:
        num_dice = int(sys.argv[1])
        if num_dice <= 0 or num_dice > 10:
            print("Please enter a number between 1 and 10.")
            sys.exit(1)
    except ValueError:
        print("Please enter a valid number.")
        sys.exit(1)

    main(num_dice)
