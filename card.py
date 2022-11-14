import random


class Card:
    bingo = ["B", "I", "N", "G", "O"]
    col_range = {"B": (1, 15), "I": (16, 30), "N": (31, 45), "G": (46, 60), "O": (61, 75)}

    def __init__(self):
        self.grid = [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]]
        self.randomize_card()
        self.state = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]

    def randomize_card(self):
        for row in range(len(self.grid)):
            num_range = self.col_range[self.bingo[row]]
            self.grid[row] = random.sample(range(num_range[0], num_range[1]), 5)
        self.grid = [list(x) for x in zip(*self.grid)]
        self.grid[2][2] = "★"

    def update_card(self, row, col):
        self.state[row][col] = 1
        print(self)

    def check_win(self):
        # Check row
        for row in self.state:
            if sum(row) == 5:
                return True

        # Check column
        for col in range(len(self.state)):
            column = [self.state[row][col] for row in range(len(self.state))]
            if sum(column) == 5:
                return True

        # Check diagonal
        if self.state[0][0] + self.state[1][1] + self.state[2][2] + self.state[3][3] + self.state[4][4] == 5:
            return True
        if self.state[0][4] + self.state[1][3] + self.state[2][2] + self.state[3][1] + self.state[4][0] == 5:
            return True

        # Does not satisfy win conditions:
        return False

    def __str__(self):
        s = " ".join(char.rjust(2) for char in self.bingo) + "\n"
        for row in self.grid:
            for col in row:
                s += str(col).rjust(2) + " "
            s += "\n"
        return s


if __name__ == "__main__":
    card = Card()
    print(card)
