#20260217
# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import random
from enum import Enum
from collections import Counter
import time


class Move(Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


class Player:
    def __init__(self, name):
        self.name = name
        self.stats = Counter()

    def move(self):
        # ran from an enum
        # time.sleep(1)
        return random.choice(list(Move))

    def recordResult(self, result):
        self.stats[result] += 1

    def rates(self, total_rounds):
        performance = {"wins": 0, "losses": 0, "ties": 0}
        performance["wins"] = self.stats["wins"] / total_rounds
        performance["losses"] = self.stats["losses"] / total_rounds
        performance["ties"] = self.stats["ties"] / total_rounds
        return performance


class Game:
    def __init__(self, rounds):
        self.rounds = rounds
        self.p1 = Player("P1")
        self.p2 = Player("P2")

    def which_winner(self, m1, m2):
        ret = None
        if m1 == m2:
            ret = "tie"
            return ret

        win_dict = {
            Move.ROCK: Move.SCISSORS,
            Move.SCISSORS: Move.PAPER,
            Move.PAPER: Move.ROCK
        }
        ret = "win" if win_dict[m1] == m2 else "loss"
        return ret

    def play(self):
        # record
        for _ in range(self.rounds):
            m1 = self.p1.move()
            m2 = self.p2.move()

            print("Moves:")
            print(m1)
            print(m2)

            result1 = self.which_winner(m1, m2)
            # Question --
            # result2 = self.which_winner(m2,m1)
            result2 = (
                "tie" if result1 == "tie"
                else "loss" if result1 == "win"
                else "win"  # if result1 == "loss"
            )
            self.p1.recordResult(result1)
            self.p2.recordResult(result2)

    def report(self):
        r1 = self.p1.rates(self.rounds)
        r2 = self.p2.rates(self.rounds)
        print(f"{self.p1.name}")
        print(f"{r1['wins']}")
        print(f"{r1['losses']}")
        print(f"{r1['ties']}")

        print(f"{self.p2.name}")
        print(f"{r2['wins']}")
        print(f"{r2['losses']}")
        print(f"{r2['ties']}")


# Main
g = Game(2)
g.play()
g.report()














