import numpy as np

class Computer:

    def random_think(self, B_or_W, board):
        BLANK = "×"
        options = np.empty((0, 2), int)
        for y in range(8):
            for x in range(8):
                if board.access(y,x) == BLANK:
                    reversible_othellos = board.reversible_othello(B_or_W, y, x)
                    if reversible_othellos.shape[0] > 0:
                        options = np.append(options, np.array([y,x]).reshape(1,2), axis = 0)
        option = np.random.randint(0, options.shape[0])
        return options[option]

    



