import play_NN_GA
import numpy as np
import random, copy

class Learning:

    def receive_w_matrix(self, genom):
        w1 = genom[1:51].reshape(10, 5)
        w2 = genom[51:61].reshape(1,10)
        return w1, w2

    def one_cycle(self, gas):
        score_and_w_matrixes = self.calc_score_and_w_matrix(gas)
        elite, others = self.select_elite(score_and_w_matrixes, 2)
        others = self.select_roulette(others, 8)
        son_elite1, son_elite2 = self.crossover(elite[0], elite[1])
        new_gas = np.empty((0, 61), float)
        new_gas = np.append(new_gas, elite, axis = 0)
        new_gas = np.append(new_gas, others, axis = 0)
        new_gas = np.append(new_gas, son_elite1, axis = 0)
        new_gas = np.append(new_gas, son_elite2, axis = 0)
        for j in range(19):
                first, second = np.random.randint(0, 50, 2)
                new_first, new_second = self.crossover(score_and_w_matrixes[first], score_and_w_matrixes[second])
                new_gas = np.append(new_gas, new_first, axis = 0)
                new_gas = np.append(new_gas, new_second, axis = 0)
        new_gas = self.mutation(new_gas, 0.2, 0.2)
        
        return new_gas


    def calc_score_and_w_matrix(self, gas):
        score_and_w_matrixes = np.empty((0, 61), float)
        for i in range(100):
            w1, w2 = self.receive_w_matrix(gas[i])
            score_and_w_matrixes = np.append(score_and_w_matrixes, play_NN_GA.Othello().play(w1, w2).reshape(1, 61), axis = 0)
        
        return score_and_w_matrixes

    def select_elite(self, score_and_w_matrixes, elite_length):
        col_num = 0
        score_and_w_matrixes_sort_col_num = score_and_w_matrixes[np.argsort(score_and_w_matrixes[:, col_num])[::-1]]
        elite, others = score_and_w_matrixes_sort_col_num[:elite_length], score_and_w_matrixes_sort_col_num[elite_length:]
        return elite, others
    
    def select_roulette(self, others, roulette_length):
        select_list = np.empty((0, 61), float)
        abs_min_score = abs(others[others.shape[0]-1][0])
        roulette_box = []
        i = 0
        for other in others:
            for j in range(max(1,int(10*(other[0] + abs_min_score)))):
                roulette_box.append(i)
            i += 1

        for k in range(roulette_length):
            idx = random.randint(0, len(roulette_box)-1)
            choice_idx = roulette_box[idx]
            select_list = np.append(select_list, others[choice_idx].reshape(1, 19), axis = 0)

        return select_list
        
    def crossover(self, ga_first, ga_second):
        point_first = random.randint(1, 60)
        point_second = random.randint(point_first, 60)
        new_first = np.concatenate([ga_first[:point_first], ga_second[point_first:point_second], ga_first[point_second:]]).reshape(1, 61)
        new_second = np.concatenate([ga_second[:point_first], ga_first[point_first:point_second], ga_second[point_second:]]).reshape(1, 61)
        return new_first, new_second

    def mutation(self, gas, individual_mutation, genom_mutation):
        ga_list = np.empty((0, 61) ,float)
        for i in gas:
            if individual_mutation > (random.randint(0, 100) / 100.0):
                mutation_genom = np.array([i[0]])
                for genom in i[1:]:
                    if genom_mutation > (random.randint(0, 100) / 100.0):
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
    for i in range(50):
        tmp1 = np.array([0])
        tmp2 = np.random.rand(60)
        tmp = np.append(tmp1, tmp2)
        gas = np.append(gas, tmp.reshape(1, 61), axis = 0)

    for i in range(100):
        gas = Learning().one_cycle(gas)
    
    col_num = 0
    gas_col_num = gas[np.argsort(gas[:, col_num])[::-1]]
    with open('NN_w_matrix.txt', 'w') as f:
        print(gas_col_num, file=f)
"""

