import numpy as np

class Board:
    
    def __init__(self):
        BLACK = "●" 
        WHITE = "○" 
        BLANK = "×" 
        # オセロ盤を初期化
        self.board = np.full((8, 8), BLANK)
        self.board[3][3] = BLACK
        self.board[4][4] = BLACK
        self.board[3][4] = WHITE
        self.board[4][3] = WHITE

    def print(self): # 盤面を表示させる
        print(self.board)

    def access(self, y, x): # マス目にアクセス
        return self.board[y][x]

    def put(self, y, x, new): # マス目を書き換え
        self.board[y][x] = new

    def is_playable(self): 
        BLANK = "×" 
        # 空きマスが有り:True, 全て石で埋まっている:False
        return np.any(self.board == BLANK)

    def reversible_othello(self, B_or_W, y, x):
        BLACK = "●" 
        WHITE = "○" 
        # (y,x)に石を置くことでひっくり返せるマスを探して返す
        reversible_othellos = np.empty((0,2), int)
        Dx = np.array([-1, 0, 1])
        Dy = np.array([-1, 0, 1])
        if B_or_W == "BLACK":
            for dy in Dy:
                for dx in Dx:
                    tmp_reversible_othellos = np.empty((0,2), int)
                    if (y == 0 and dy < 0) or (y == 7 and dy > 0) or (x == 0 and dx < 0) or (x == 7 and dx > 0): 
                        continue  
                    if dy == dx == 0:
                        continue
                    else:
                        if 0 <= y+dy <= 7 and 0 <= x+dx <= 7 and self.access(y+dy, x+dx) == WHITE: # 探索マスが盤面内かつ白石がある
                            for i in np.arange(1,8):              
                                if y+(dy*i) == 0 or y+(dy*i) == 7 or x+(dx*i) == 0 or x+(dx*i) == 7:
                                    # 角マスに石を置く場合の処理
                                    if (y, x) == (0,0):
                                        if y+(dy*i) == 7 or x+(dx*i) == 7:
                                            if self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break   

                                    elif (y, x) == (0, 7):
                                        if y+(dy*i) == 7 or x+(dx*i) == 0:
                                            if self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break                                                                        
                                
                                    elif (y, x) == (7, 0):
                                        if y+(dy*i) == 0 or x+(dx*i) == 7:
                                            if self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break  

                                    elif (y, x) == (7, 7):
                                        if y+(dy*i) == 0 or x+(dx*i) == 0:
                                            if self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break 

                                    # 角でない縁マスに石を置いた場合の処理                      
                                    elif y == 0:
                                        if y+(dy*i) == 7 or x+(dx*i) == 0 or x+(dx*i) == 7:
                                            if self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break  

                                    elif y == 7:
                                        if y+(dy*i) == 0 or x+(dx*i) == 0 or x+(dx*i) == 7:
                                            if self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break 

                                    elif x == 0:
                                        if y+(dy*i) == 0 or y+(dy*i) == 7 or x+(dx*i) == 7:
                                            if self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break  

                                    elif x == 7:
                                        if y+(dy*i) == 0 or y+(dy*i) == 7 or x+(dx*i) == 0:
                                            if self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break  

                                    # 縁でないマスに石を置き、探索が端に達した場合
                                    elif self.access(y+(dy*i), x+(dx*i)) == BLACK: 
                                        reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                        break                                       
                                    else:
                                        break
                                
                                # 縁でないマスに石を置き、探索が端に達していない場合
                                elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                    reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                    break
                                elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                    tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                else:
                                    break                   

        else:
            for dy in Dy:
                for dx in Dx:
                    tmp_reversible_othellos = np.empty((0,2), int)
                    if (y == 0 and dy < 0) or (y == 7 and dy > 0) or (x == 0 and dx < 0) or (x == 7 and dx > 0):
                        continue  
                    if dy == dx == 0:
                        continue
                    else:
                        if 0 <= y+dy <= 7 and 0 <= x+dx <= 7 and self.access(y+dy, x+dx) == BLACK: # 探索マスが盤面内かつ黒石がある
                            for i in np.arange(1,8):              
                                if y+(dy*i) == 0 or y+(dy*i) == 7 or x+(dx*i) == 0 or x+(dx*i) == 7:
                                    # 角マスに石を置く場合の処理
                                    if (y, x) == (0,0):
                                        if y+(dy*i) == 7 or x+(dx*i) == 7:
                                            if self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break   

                                    elif (y, x) == (0, 7):
                                        if y+(dy*i) == 7 or x+(dx*i) == 0:
                                            if self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break                                                                        
                                
                                    elif (y, x) == (7, 0):
                                        if y+(dy*i) == 0 or x+(dx*i) == 7:
                                            if self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break  

                                    elif (y, x) == (7, 7):
                                        if y+(dy*i) == 0 or x+(dx*i) == 0:
                                            if self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break 

                                    # 角でない縁マスに石を置いた場合の処理                      
                                    elif y == 0:
                                        if y+(dy*i) == 7 or x+(dx*i) == 0 or x+(dx*i) == 7:
                                            if self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break  

                                    elif y == 7:
                                        if y+(dy*i) == 0 or x+(dx*i) == 0 or x+(dx*i) == 7:
                                            if self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break 

                                    elif x == 0:
                                        if y+(dy*i) == 0 or y+(dy*i) == 7 or x+(dx*i) == 7:
                                            if self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break  

                                    elif x == 7:
                                        if y+(dy*i) == 0 or y+(dy*i) == 7 or x+(dx*i) == 0:
                                            if self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                                reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                                break                                       
                                            else:
                                                break

                                        elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                            reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                            break
                                        elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                            tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                        else:
                                            break  

                                    # 縁でないマスに石を置き、探索が端に達した場合
                                    elif self.access(y+(dy*i), x+(dx*i)) == WHITE: 
                                        reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                        break                                       
                                    else:
                                        break
                                
                                # 縁でないマスに石を置き、探索が端に達していない場合
                                elif self.access(y+(dy*i), x+(dx*i)) == WHITE:
                                    reversible_othellos = np.append(reversible_othellos, tmp_reversible_othellos, axis = 0)
                                    break
                                elif self.access(y+(dy*i), x+(dx*i)) == BLACK:
                                    tmp_reversible_othellos = np.append(tmp_reversible_othellos, np.array([y+(dy*i), x+(dx*i)]).reshape(1,2), axis = 0)  
                                else:
                                    break                   

        return reversible_othellos              

    def is_pass(self, B_or_W):
        BLANK = "×" 
        # 石を置くことでひっくり返せる空きマスがあればFalse
        for y in range(8):
            for x in range(8):
                if self.access(y, x) ==  BLANK:
                    reversible_othellos = self.reversible_othello(B_or_W, y, x)
                    if reversible_othellos.shape[0] > 0:
                        return False          
        
        return True


    def is_OK(self, B_or_W, y, x):
        BLANK = "×" 
        # 打つマスがオセロ盤内かつ石をひっくり返せるような空きマスならばTrue
        reversible_othellos = self.reversible_othello(B_or_W, y, x)
        if 0 <= y <= 7 and 0 <= x <= 7 and self.access(y,x) == BLANK and reversible_othellos.shape[0] > 0:
            return True
        else:
            return False
    
    def reverse_othello(self, B_or_W, Y, X):
        BLACK = "●" 
        WHITE = "○" 
        # 石を置き、置くことでひっくり返せる石をひっくり返した後の盤面を返す
        reversible_othellos = self.reversible_othello(B_or_W, Y, X)
        if B_or_W == "BLACK":
            self.put(Y, X, BLACK)  
            for reversible_othello in reversible_othellos:
                y = reversible_othello[0]
                x = reversible_othello[1]
                self.put(y, x, BLACK) 

        else:
            self.put(Y, X, WHITE) 
            for reversible_othello in reversible_othellos:
                y = reversible_othello[0]
                x = reversible_othello[1]
                self.put(y, x, WHITE) 
        

    
    def count_stones(self): # 黒石、白石の個数をカウント
        blacks = np.count_nonzero(self.board == "●")
        whites = np.count_nonzero(self.board == "○") 
        return (blacks, whites) 

