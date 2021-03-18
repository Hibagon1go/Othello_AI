import play_NN_GA
import numpy as np
import random, copy

class Learning:

    # 一次元配列から重み行列を取り出す
    def receive_w_matrix(self, genom):
        w1 = genom[1:51].reshape(10, 5)
        w2 = genom[51:61].reshape(1,10)
        return w1, w2

    # 1世代で行う遺伝的アルゴリズムの処理
    def one_cycle(self, gas):
        score_and_w_matrixes = self.calc_score_and_w_matrix(gas) # 引数で受け取った世代のオセロAI同士を総当たりで戦わせて、各個体のスコア(強さ)を計算
        elite, others = self.select_elite(score_and_w_matrixes, 2) # スコアの良い個体2個体をエリートとして次世代に残す
        others = self.select_roulette(others, 5) # その他に、スコアの高い個体を中心に5個体を次世代に残す
        son_elite1, son_elite2 = self.crossover(elite[0], elite[1]) # エリートの子供を作り、それも次世代に残す
        # 残す個体を次世代(new_gas)に追加していく
        new_gas = np.empty((0, 61), float)
        new_gas = np.append(new_gas, elite, axis = 0)
        new_gas = np.append(new_gas, others, axis = 0)
        new_gas = np.append(new_gas, son_elite1, axis = 0)
        new_gas = np.append(new_gas, son_elite2, axis = 0)
        # 最後に現世代から、スコアの高い個体を中心に親を選び、その子供を作ることで16個体を次世代に残す
        for j in range(8):
                parents = self.select_roulette(score_and_w_matrixes, 2)
                parents1, parents2 = parents[0], parents[1]
                new_first, new_second = self.crossover(parents1, parents2)
                new_gas = np.append(new_gas, new_first, axis = 0)
                new_gas = np.append(new_gas, new_second, axis = 0)
        # 次世代の個体に一定確率で突然変異を起こす
        new_gas = self.mutation(new_gas, 0.2, 0.2)
        
        return new_gas

# 引数で受け取った世代のオセロAI同士を総当たりで戦わせて、各個体のスコア(強さ)を計算
    def calc_score_and_w_matrix(self, gas):
        score_and_w_matrixes = np.empty((0, 61), float)
        for i in range(25):
            score = 0
            w1, w2 = self.receive_w_matrix(gas[i]) # 引数で受け取った世代のi番目の個体の重み行列を受け取る

            for j in range(25):
                w1_2, w2_2 = self.receive_w_matrix(gas[j]) # 引数で受け取った世代のj番目の個体の重み行列を受け取る
                score += play_NN_GA.Othello().play(w1, w2, w1_2, w2_2) # i番目とj番目の個体を戦わせて、i番目の個体が勝てばスコア1を獲得

            # 重み行列とスコアを一次元の配列にして返す
            tmp = np.append(w1.flatten(), w2.flatten())
            score_and_w_matrix = np.array([score])
            score_and_w_matrix = np.append(score_and_w_matrix, tmp)
            score_and_w_matrixes = np.append(score_and_w_matrixes, score_and_w_matrix.reshape(1, 61), axis = 0)
        
        return score_and_w_matrixes

    # エリートとその他を分ける
    def select_elite(self, score_and_w_matrixes, elite_length):
        col_num = 0
        score_and_w_matrixes_sort_col_num = score_and_w_matrixes[np.argsort(score_and_w_matrixes[:, col_num])[::-1]] # スコアの大きい順にソート
        elite, others = score_and_w_matrixes_sort_col_num[:elite_length], score_and_w_matrixes_sort_col_num[elite_length:] # 上からelite_length個をエリートとして残す
        return elite, others
    
    # 個体のセットから、スコアの大きい個体中心に選ぶ
    def select_roulette(self, gas, roulette_length):
        select_list = np.empty((0, 61), float)
        roulette_box = []
        i = 0
        # 各個体のスコアの分だけ、その個体のindexをルーレット箱に追加
        for kotai in gas:
            for j in range(int(kotai[0])):
                roulette_box.append(i)
            i += 1
        # roulette_length回、ランダムにルーレット箱からindexをピックアップし、そのindexの個体をselect_listに追加
        for k in range(roulette_length):
            idx = random.randint(0, len(roulette_box)-1)
            choice_idx = roulette_box[idx]
            select_list = np.append(select_list, gas[choice_idx].reshape(1, 61), axis = 0)

        return select_list
        
    # 2つの親個体の重み行列の一部を交換
    def crossover(self, ga_first, ga_second):
        # point_first番目からpoint_second番目までの重み行列の値をを交換
        point_first = random.randint(1, 60) 
        point_second = random.randint(point_first, 60)
        new_first = np.concatenate([ga_first[:point_first], ga_second[point_first:point_second], ga_first[point_second:]]).reshape(1, 61)
        new_second = np.concatenate([ga_second[:point_first], ga_first[point_first:point_second], ga_second[point_second:]]).reshape(1, 61)
        return new_first, new_second

    # 重み行列に、一定確率で突然変異を引き起こす
    def mutation(self, gas, individual_mutation, genom_mutation):
        ga_list = np.empty((0, 61) ,float)
        for i in gas:
            if individual_mutation > (random.randint(0, 100) / 100.0): # individual_mutation % の確率で、個体iに突然変異を引き起こす
                mutation_genom = np.array([i[0]])
                for genom in i[1:]:
                    if genom_mutation > (random.randint(0, 100) / 100.0): # genom_mutation % の確率で、個体iの重み行列の値genomに突然変異を引き起こす
                        mutation_genom = np.append(mutation_genom, np.random.normal(0.0,1.0))  
                    else:
                        mutation_genom = np.append(mutation_genom, genom) 

                ga_list = np.append(ga_list, mutation_genom.reshape(1, 61), axis = 0)
            else:
                ga_list = np.append(ga_list, i.reshape(1, 61), axis = 0)
        return ga_list       


"""
if __name__ == '__main__':
    gas = np.empty((0, 61), float)
    for i in range(25):
        tmp1 = np.array([0])
        tmp2 = np.random.rand(60)
        tmp = np.append(tmp1, tmp2)
        gas = np.append(gas, tmp.reshape(1, 61), axis = 0)

    for i in range(50):
        gas = Learning().one_cycle(gas)
    
    col_num = 0
    gas_col_num = gas[np.argsort(gas[:, col_num])[::-1]]
    with open('NN_w_matrix.txt', 'w') as f:
        print(gas_col_num, file=f)
"""

