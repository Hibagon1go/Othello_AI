import boards, nn
import numpy as np
import random

class Othello:

    def play(self, w1, w2, w1_2, w2_2):
        board = boards.Board() # オセロ盤インスタンスを生成

        B_or_W = "BLACK"
        
        computer1 = nn.NN() # コンピューター1インスタンスを生成
        computer2 = nn.NN() # コンピューター2インスタンスを生成

        total_moves = 0 # 総手数を初期化

        while board.is_playable() and not(board.is_pass("BLACK") and board.is_pass("WHITE")): # ゲーム終了(全てのマスが埋まる or 両プレイヤーがパス)が訪れるまでループ
            # -------------------------------------------コンピューター1の手番の処理------------------------------------------- #
            if not board.is_pass("BLACK"):
                total_moves += 1 
                y, x = computer1.nn_think(w1, w2, board) # コンピューター1の打つマスを決定し、受け取り
                board.reverse_othello("BLACK", y, x) 
 
            # -----------------------------------------コンピューター2の手番の処理----------------------------------------- #
            if not board.is_pass("WHITE"):
                total_moves += 1 
                y, x = computer2.nn_think(w1_2, w2_2, board) # コンピューター2の打つマスを決定し、受け取り
                board.reverse_othello("WHITE", y, x)
       
        self.show_result(B_or_W, board) # 最終結果表示
        blacks, whites = board.count_stones()
        if blacks > whites:
            score = 1
        else:
            score = 0
            
        return score


    def show_result(self, B_or_W, board):
        blacks, whites = board.count_stones()
        board.print()
        print("----------最終結果----------")
        print("コンピューター1:{}, コンピューター2:{}".format(blacks, whites))
        if blacks > whites:
            print("コンピューター1の勝ちです。")
        elif whites > blacks:
            print("コンピューター2の勝ちです。")
        else:
            print("引き分けです。")

if __name__ == '__main__':
    Othello().play()
    




            





            
