import boards, nn

class Othello:

    def play(self):
        board = boards.Board() # オセロ盤インスタンスを生成

        B_or_W = ""
        while B_or_W != "BLACK" and B_or_W != "WHITE": # 正しい入力がなされるまでループ
            B_or_W = input("先手を選択する場合BLACK, 後手を選ぶ場合WHITEと入力して下さい。") # ユーザーの先手後手を選択
        
        computer = nn.NN() # コンピューターインスタンスを生成

        total_moves = 0 # 総手数を初期化

        while board.is_playable() and not(board.is_pass("BLACK") and board.is_pass("WHITE")): # ゲーム終了(全てのマスが埋まる or 両プレイヤーがパス)が訪れるまでループ
            if B_or_W == "BLACK": # ユーザーが先手の場合
                # -------------------------------------------ユーザーの手番の処理------------------------------------------- #
                if board.is_pass("BLACK"): # パスするしかない場合
                    print("あなたはパスしました。")
                    
                else:
                    total_moves += 1 
                    print(str(total_moves) + "手目です。") 
                    blacks, whites = board.count_stones()
                    print("あなた:{},コンピューター:{}".format(blacks, whites))
                    board.print()

                    y, x = 100, 100 # ユーザーの打つマスを初期化
                    while not board.is_OK("BLACK", y, x): # ユーザーがルール上OKの場所に打つまでループ
                        y, x = map(int,input("あなたの手を入力して下さい。(上から何行目?,左から何列目?)").split()) # ユーザーの打つマスを受け取り
                        y -= 1
                        x -= 1

                    board.reverse_othello("BLACK", y, x) # オセロをひっくり返し、盤面を更新

                # -----------------------------------------コンピューターの手番の処理----------------------------------------- #
                if board.is_pass("WHITE"): 
                    print("コンピューターはパスしました。")
                    continue
                
                else:
                    total_moves += 1 
                    print(str(total_moves) + "手目です。")
                    blacks, whites = board.count_stones()
                    print("あなた:{},コンピューター:{}".format(blacks, whites))
                    board.print()
                    print("コンピューターは考え中です...")

                    y, x = computer.nn_think(board) # コンピューターの打つマスを決定し、受け取り

                    board.reverse_othello("WHITE", y, x) 
                    board.print()

            else: # ユーザーが後手の場合
                # -----------------------------------------コンピューターの手番の処理----------------------------------------- #
                if board.is_pass("BLACK"): 
                    print("コンピューターはパスしました。")
                    continue
                
                else:
                    total_moves += 1
                    print(str(total_moves) + "手目です。") 
                    blacks, whites = board.count_stones()
                    print("コンピューター:{},あなた:{}".format(blacks,whites))
                    board.print()
                    print("コンピューターは考え中です...")

                    y, x = computer.nn_think(board)

                    board.reverse_othello("BLACK", y, x)
                    board.print() 
    
                # -------------------------------------------ユーザーの手番の処理------------------------------------------- #
                if board.is_pass("WHITE"): 
                    print("あなたはパスしました。")

                else:
                    total_moves += 1 
                    print(str(total_moves) + "手目です。") 
                    blacks, whites = board.count_stones()
                    print("コンピューター:{},あなた:{}".format(blacks,whites))
                    board.print()

                    y, x = 100,100 
                    while not board.is_OK("WHITE", y, x): 
                        y, x = map(int,input("あなたの手を入力して下さい。(上から何行目?,左から何列目?)").split()) 
                        y -= 1
                        x -= 1
            
                    board.reverse_othello("WHITE", y, x)

        
        self.show_result(B_or_W, board) # 最終結果表示

    def show_result(self, B_or_W, board):
        blacks, whites = board.count_stones()
        board.print()
        print("----------最終結果----------")
        if B_or_W == "BLACK":
            print("あなた:{}, コンピューター:{}".format(blacks, whites))
            if blacks > whites:
                print("あなたの勝ちです。")
            elif whites > blacks:
                print("コンピューターの勝ちです。")
            else:
                 print("引き分けです。")
        elif B_or_W == "WHITE":
            print("コンピューター:{}, あなた:{}".format(blacks, whites))
            if blacks > whites:
                print("コンピューターの勝ちです。")
            elif whites > blacks:
                print("あなたの勝ちです。")
            else:
                 print("引き分けです。")



if __name__ == '__main__':
    Othello().play()

            





            





        






