import numpy as np

class Computer:

    def random_think(self, B_or_W, board):
        BLANK = "×"
        now_availables = board.availables(B_or_W)
        choice = np.random.randint(0, now_availables.shape[0])
        return now_availables[choice]

    



