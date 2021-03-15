import play_NN_GA
import numpy as np

class Learning:

    def learning(self):
        score_and_w_matrixes = np.empty((0, 19), float)
        for i in range(10):
            othello = play_NN_GA.Othello()
            score_and_w_matrixes = np.append(score_and_w_matrixes, othello.play().reshape(1, 19), axis = 0)
        
        col_num = 0
        score_and_w_matrixes_sort_col_num = score_and_w_matrixes[np.argsort(score_and_w_matrixes[:, col_num])[::-1]]
        return score_and_w_matrixes_sort_col_num

if __name__ == '__main__':
    w_best_100 = Learning().learning()
    with open('NN_w_matrix.txt', 'w') as f:
        print(w_best_100, file=f)

