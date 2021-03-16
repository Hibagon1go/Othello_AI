import play_NN_GA
import numpy as np
import random, copy

class Learning:

    def receive_w_matrix(self, genom):
        w1 = genom[1:16].reshape(3, 5)
        w2 = genom[16:19].reshape(1,3)
        return w1, w2

    def one_cycle(self, gas):
        score_and_w_matrixes = self.calc_score_and_w_matrix(gas)
        elite, others = self.select_elite(score_and_w_matrixes, 5)
        others = self.select_roulette(others, 5)
        gas = np.append(elite, others, axis = 0)
        for j in range(10):
                first, second = np.random.randint(0, 10, 2)
                new_first, new_second = self.crossover(gas[first], gas[second])
                new_gas = np.append(new_gas, new_first, axis = 0)
                new_gas = np.append(new_gas, new_second, axis = 0)
        new_gas = self.mutation(new_gas, 10, 30)
        
        return new_gas


    def calc_score_and_w_matrix(self, gas):
        score_and_w_matrixes = np.empty((0, 19), float)
        for i in range(20):
            w1, w2 = self.receive_w_matrix(gas[i])
            score_and_w_matrixes = np.append(score_and_w_matrixes, play_NN_GA.Othello().play(w1, w2).reshape(1, 19), axis = 0)
        
        return score_and_w_matrixes

    def select_elite(self, score_and_w_matrixes, elite_length):
        col_num = 0
        score_and_w_matrixes_sort_col_num = score_and_w_matrixes[np.argsort(score_and_w_matrixes[:, col_num])[::-1]]
        elite, others = score_and_w_matrixes_sort_col_num[:elite_length], score_and_w_matrixes_sort_col_num[elite_length:]
        return elite, others
    
    def select_roulette(self, others, roulette_length):
        others_copy = copy.deepcopy(others)
        total = 0
        select_list = np.empty((0, 19), float)
        for other in others_copy:
            total += other[0]
        for i in range(roulette_length):
            Vsum = 0
            arrow = random.randint(0, total-1)
            for other in others_copy:
                Vsum += other[0]
                if Vsum > arrow:
                    select_list = np.append(select_list, other, axis = 0)
                    total -= other[0]
                    others_copy.remove(other)
                    break

        return select_list
        
    def crossover(self, ga_first, ga_second):
        point_first = random.randint(0, 18)
        point_second = random.randint(point_first, 18)
        first = ga_first[point_first]
        second = ga_second[point_second]
        new_first = np.concatenate([first[:point_first], second[point_first:point_second], first[point_second:]])
        new_second = np.concatenate([second[:point_first], first[point_first:point_second], second[point_second:]])  
        return new_first, new_second

    def mutation(self, gas, individual_mutation, genom_mutation):
        ga_list = np.array([])
        for i in gas:
            if individual_mutation > (random.randint(0, 100) / 100.0):
                genom_list = np.array([])
                for genom in i:
                    if genom_mutation > (random.randint(0, 100) / 100.0):
                        genom_list = np.append(genom_list, np.random.normal(0.0,1.0))  
                    else:
                        genom_list = np.append(genom_list, genom) 
            else:
                ga_list = np.append(ga_list, i)
        return ga_list       


if __name__ == '__main__':
    gas = np.empty((0, 19), float)
    for i in range(20):
        tmp1 = np.array([0])
        tmp2 = np.random.rand(18)
        tmp = np.append(tmp1, tmp2)
        gas = np.append(gas, tmp.reshape(1, 19), axis = 0)

    for i in range(10):
        gas = Learning().one_cycle(gas)
    
    col_num = 0
    gas_col_num = gas[np.argsort(gas[:, col_num])[::-1]]
    with open('NN_w_matrix.txt', 'w') as f:
        print(gas_col_num, file=f)

