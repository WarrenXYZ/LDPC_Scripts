import random
import numpy as np


def gen_initial_codeword(n):
    codeword_array = np.random.randint(0, 2, n)
    codeword_list = list(codeword_array)
    return codeword_list

def apply_channel(n, error_rate, p_key):
    for i in range(n):
        temp_random = random.random()
        if temp_random < error_rate:
            # print(temp_random)
            if p_key[i] == 0:
                p_key[i] = 1
            elif p_key[i] == 1:
                p_key[i] = 0
            else:
                print("p_key wrong!")

    return p_key

def save_codeword_file(filename, n, codeword):
    file = open(filename, 'w')
    for i in range(n):
        file.write(str(codeword[i]) + ' ')

    file.write('\n')
    file.close()

if __name__ == '__main__':
    # p_key = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # error_rate = 0.5
    # n = len(p_key)
    #
    # q_key = apply_channel(n, error_rate, p_key)
    # print(q_key)
    #
    # m = 20
    # err = 0.01
    # p = gen_initial_codeword(m)
    # print(p)
    # q = apply_channel(m, err, p)
    # print(q)
    # filename = '0.txt'
    # save_codeword_file(filename, m, q)
    # save_codeword_file(filename, m, q)

    len_codeword = 100000

    code_rate = [0.75, 0.8, 0.85]
    top_error_rate = [0.0415, 0.032, 0.0215]
    test_error_rate = [0.039, 0.028, 0.018]

    p_key = gen_initial_codeword(len_codeword)
    save_codeword_file('initial_codeword_100000.txt', len_codeword, p_key)
    for i in range(3):
        q_key = apply_channel(len_codeword, test_error_rate[i], p_key)
        txt_name = "codeword_100000_{}_{}.txt".format(code_rate[i], test_error_rate[i])
        save_codeword_file(txt_name, len_codeword, q_key)