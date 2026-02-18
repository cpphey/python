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
        ret= random.choice(list(Move))
        return ret

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
            ret = "ties" #BUG - was missing s
            return ret

        win_dict = {
            Move.ROCK: Move.SCISSORS,
            Move.SCISSORS: Move.PAPER,
            Move.PAPER: Move.ROCK
        }
        ret = "wins" if win_dict[m1] == m2 else "losses" #BUG - was missing s
        return ret

    def play(self):
        # record
        for _ in range(self.rounds):
            m1 = self.p1.move()
            m2 = self.p2.move()

            result1 = self.which_winner(m1, m2)
            # Question --
            # result2 = self.which_winner(m2,m1)
            result2 = (
                "ties" if result1 == "ties"
                else "losses" if result1 == "wins"
                else "wins"  # if result1 == "loss"
            )
            #if result1 != "tie":
            print("Round ",_," ",self.p1.name, " : ", m1, " result: ", result1)
            print("Round ",_," ",self.p2.name, " : ", m2, " result: ", result2)
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
g = Game(10)
g.play()
g.report()














