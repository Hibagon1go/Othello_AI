import numpy as np
import copy

class NN:

    # シグモイド関数
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    # 特徴量ベクトルを生成
    def create_vector(self, B_or_W, board):
        now_board = copy.deepcopy(board)
        corners = np.array([now_board.access(0, 0), now_board.access(0, 7), now_board.access(7, 0), now_board.access(7, 7)]) 
        mid_corners = np.array([now_board.access(2, 2), now_board.access(2, 5), now_board.access(5, 2), now_board.access(5, 5)])
        centers = np.array([now_board.access(3, 3), now_board.access(3, 4), now_board.access(4, 3), now_board.access(4, 4)])
        if B_or_W == "BLACK": # 先手の場合
             dif_corners = np.count_nonzero(corners == "●") - np.count_nonzero(corners == "○") # 角の黒石と白石の個数の差
             dif_mid_corners = np.count_nonzero(mid_corners == "●") - np.count_nonzero(mid_corners == "○") # 真ん中の黒石と白石の個数の差
             dif_centers = np.count_nonzero(centers == "●") - np.count_nonzero(centers == "○") # 真ん中4×4の角の黒石と白石の個数の差
             blacks, whites = now_board.count_stones() 
             dif_stones = blacks - whites # 現在の盤面の黒石と白石の個数の差
             num_availables = now_board.availables("WHITE").shape[0] # 現在後手が打つことのできるマス目の数
        
        else: # 後手の場合
             dif_corners = np.count_nonzero(corners == "○") - np.count_nonzero(corners == "●")
             dif_mid_corners = np.count_nonzero(mid_corners == "○") - np.count_nonzero(mid_corners == "●")
             dif_centers = np.count_nonzero(centers == "○") - np.count_nonzero(centers == "●")
             blacks, whites = now_board.count_stones()
             dif_stones = whites - blacks
             num_availables = now_board.availables("BLACK").shape[0]
             
        # num_blanks = np.count_nonzero(now_board == "×")

        vector = np.array([dif_corners, dif_mid_corners, dif_centers, dif_stones, num_availables]).reshape(5,1)
        return vector
    
    # 盤面の評価値を計算
    def evaluation(self, B_or_W, w1 , w2, board):
        vector = self.create_vector(B_or_W, board)
        mid_vec = np.dot(w1, vector) # 重み行列と特徴量ベクトルの積
        values = np.dot(w2, mid_vec) # 重み行列とmid_vecの積
        return self.sigmoid(values) # valuesのシグモイド関数を作用しこれを評価値とする
    
    # 次に打つ手を決定
    def nn_think(self, B_or_W, w1, w2, board):
        now_availables = board.availables(B_or_W)
        Now_board = copy.deepcopy(board)
        options = np.empty((0, 3), float) # 打つマスの選択肢を格納する
        for available in now_availables:
            next_board = copy.deepcopy(Now_board) # 現在の盤面
            # 今回考える手(y, x)
            y = available[0] 
            x = available[1]
            next_board.reverse_othello(B_or_W, y, x) # (y, x)に打ち、仮想的に盤面を更新
            values = self.evaluation(B_or_W, w1, w2, next_board) # その場合の評価値を計算
            options = np.append(options, np.array([values, y, x]).reshape(1, 3), axis = 0) # 評価値と打つマス目のセットをoptionsに追加

        col_num = 0
        options_sort_col_num = options[np.argsort(options[:, col_num])[::-1]] # 評価値の大きい順にソート
        return options_sort_col_num[0][1:] # 評価値の最も大きくなる手を返す

    


        
        
    
