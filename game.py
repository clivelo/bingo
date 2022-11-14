import random
from card import Card


def main():
    card = Card()
    print(card)
    bingo_seq = random.sample(range(1, 76), 75)
    num = 0
    while not card.check_win():
        roll = bingo_seq[num]
        char = [k for k, v in Card.col_range.items() if v[0] <= roll <= v[1]][0]
        print(f"{char} {roll}")
        action = input("Enter / if no action; Enter 2,2 to circle row 3 column 3: ")
        if action == "/":
            pass
        else:
            card.update_card(int(action[0]), int(action[-1]))
        num += 1
        print("\r")


if __name__ == "__main__":
    main()
