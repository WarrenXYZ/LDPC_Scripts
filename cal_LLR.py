import math
from gen_codewords import gen_initial_codeword, apply_channel


def cal_llr_BSC(n, error_rate, codeword):
    """
    Calculate the LLR of codeword received
    :param n:               the length of codeword
    :param error_rate:      the error rate of the BSC channel
    :param codeword:        the codeword Bob received
    :return:                the list of the codeword's LLR
    """
    llr_list = []
    for i in range(n):
        if codeword[i] == 0:
            temp_llr = math.log((1 - error_rate) / error_rate)
            llr_list.append(temp_llr)
        elif codeword[i] == 1:
            temp_llr = math.log(error_rate / (1 - error_rate))
            llr_list.append(temp_llr)
        else:
            print("wrong in codeword!")
    return llr_list

if __name__ == '__main__':
    n = 10
    e = 0.3
    codeword_a = gen_initial_codeword(n)
    print(codeword_a)
    codeword_b = apply_channel(n, e, codeword_a)
    print(codeword_b)
    llr = cal_llr_BSC(n, e, codeword_b)
    print(llr)


