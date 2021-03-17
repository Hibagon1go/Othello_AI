import numpy as np
import copy

class NN:

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
     
    def create_vector(self, B_or_W, board):
        now_board = copy.deepcopy(board)
        corners = np.array([now_board.access(0, 0), now_board.access(0, 7), now_board.access(7, 0), now_board.access(7, 7)])
        mid_corners = np.array([now_board.access(2, 2), now_board.access(2, 5), now_board.access(5, 2), now_board.access(5, 5)])
        centers = np.array([now_board.access(3, 3), now_board.access(3, 4), now_board.access(4, 3), now_board.access(4, 4)])
        if B_or_W == "BLACK":
             dif_corners = np.count_nonzero(corners == "●") - np.count_nonzero(corners == "○")
             dif_mid_corners = np.count_nonzero(mid_corners == "●") - np.count_nonzero(mid_corners == "○")
             dif_centers = np.count_nonzero(centers == "●") - np.count_nonzero(centers == "○")
             blacks, whites = now_board.count_stones()
             dif_stones = blacks - whites
             num_availables = now_board.availables("BLACK").shape[0]
        
        else:
             dif_corners = np.count_nonzero(corners == "○") - np.count_nonzero(corners == "●")
             dif_mid_corners = np.count_nonzero(mid_corners == "○") - np.count_nonzero(mid_corners == "●")
             dif_centers = np.count_nonzero(centers == "○") - np.count_nonzero(centers == "●")
             blacks, whites = now_board.count_stones()
             dif_stones = whites - blacks
             num_availables = now_board.availables("WHITE").shape[0]
             
        # num_blanks = np.count_nonzero(now_board == "×")

        vector = np.array([dif_corners, dif_mid_corners, dif_centers, dif_stones, num_availables]).reshape(5,1)
        return vector
    
    def evaluation(self, B_or_W, w1 , w2, board):
        vector = self.create_vector(B_or_W, board)
        mid_vec = np.dot(w1, vector)
        values = np.dot(w2, mid_vec)
        return self.sigmoid(values)
    
    def nn_think(self, B_or_W, w1, w2, board):
        now_availables = board.availables(B_or_W)
        Now_board = copy.deepcopy(board)
        options = np.empty((0, 3), float)
        for available in now_availables:
            next_board = copy.deepcopy(Now_board)
            y = available[0]
            x = available[1]
            next_board.reverse_othello(B_or_W, y, x)
            values = self.evaluation(B_or_W, w1, w2, next_board)
            options = np.append(options, np.array([values, y, x]).reshape(1, 3), axis = 0)

        col_num = 0
        options_sort_col_num = options[np.argsort(options[:, col_num])[::-1]]
        return options_sort_col_num[0][1:]

    


        
        
    
