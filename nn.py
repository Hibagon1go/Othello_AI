import numpy as np
import copy

class NN:

    def __init__(self):
        # 初期重み行列
        self.w1 = np.array([6.19639154e-01, 6.26195335e-01, 9.46288188e-01, 8.24792074e-01, 6.87153547e-01, 2.03037882e-01, 7.74963124e-01, 9.31213339e-01, 7.07087800e-01, 8.60625926e-01, 8.65532252e-01, 7.86493197e-01, 7.31500625e-01, 7.56972711e-01, 4.92497818e-01]).reshape(3, 5) # np.random.rand(3, 5)
        self.w2 = np.array([4.62403163e-01, 8.13083470e-01, 4.44770980e-01]).reshape(1, 3) # np.random.rand(1, 3)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
     
    def create_vector(self, board):
        now_board = copy.deepcopy(board)
        corners = np.array([now_board.access(0, 0), now_board.access(0, 7), now_board.access(7, 0), now_board.access(7, 7)])
        centers = np.array([now_board.access(3, 3), now_board.access(3, 4), now_board.access(4, 3), now_board.access(4, 4)])
        dif_corners = np.count_nonzero(corners == "○") - np.count_nonzero(corners == "●")
        dif_centers = np.count_nonzero(centers == "○") - np.count_nonzero(centers == "●")

        blacks, whites = now_board.count_stones()
        dif_stones = blacks - whites
        num_blanks = np.count_nonzero(now_board == "×")

        num_availables = now_board.availables("BLACK").shape[0]
        
        vector = np.array([dif_corners, dif_centers, dif_stones, num_blanks, num_availables]).reshape(5,1)
        return vector
    
    def evaluation(self, board):
        vector = self.create_vector(board)
        mid_vec = np.dot(self.w1, vector)
        values = np.dot(self.w2, mid_vec)
        return self.sigmoid(values)
    
    def nn_think(self, board):
        now_availables = board.availables("BLACK")
        Now_board = copy.deepcopy(board)
        options = np.empty((0, 3), float)
        for available in now_availables:
            next_board = copy.deepcopy(Now_board)
            y = available[0]
            x = available[1]
            next_board.reverse_othello("BLACK", y, x)
            values = self.evaluation(next_board)
            options = np.append(options, np.array([values, y, x]).reshape(1, 3), axis = 0)

        col_num = 0
        options_sort_col_num = options[np.argsort(options[:, col_num])[::-1]]
        return options_sort_col_num[0][1:]


        
        
    
