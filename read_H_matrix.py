from collections import defaultdict

def test():
    H_filename = "H_80_100000.bin"
    f = open(H_filename, 'rb')
    ch = f.read(1)
    print(ch)
    ch = f.read(1)
    print(ch)
    ch = f.read(1)
    print(ch)
    ch = f.read(1)
    print(ch)
    ch = f.read(4)
    print(ch)
    ch = f.read(4)
    i = int.from_bytes(ch, byteorder='big')
    print(i)
    f.close()
    print("*"*10)
    s = b'\xff\xff\xff\xff'
    print(int.from_bytes(s, byteorder='big', signed=False))
    print(int.from_bytes(s, byteorder='big')) # 默认无符号
    print(int.from_bytes(s, byteorder='big', signed=True))

def matrix2dictionary(filename):
    f = open(filename, 'rb')
    first_4bytes = f.read(4)
    first_num = int.from_bytes(first_4bytes, byteorder='big', signed=True)
    print(first_num)

    second_4bytes = f.read(4)
    # second_num: 最后一个有效4字节, 下一个4字节为'0xFF FF FF FF'
    second_num = int.from_bytes(second_4bytes, byteorder='big', signed=True)
    print(second_num)

    valid_items = second_num - 1
    # valid_items = 63 - 1
    i = 0
    current_row = 0
    # none_zeros = []
    nnz_dict = {}
    while i < valid_items:
        current_row_items_4bytes = f.read(4)
        current_row_items = int.from_bytes(current_row_items_4bytes, byteorder='big', signed=True)
        i += 1

        nnz_dict[current_row] = []

        for j in range(current_row_items):
            current_items_col_4bytes = f.read(4)
            current_items_col = int.from_bytes(current_items_col_4bytes, byteorder='big', signed=True)
            i += 1

            # none_zeros.append((current_row, current_items_col))
            nnz_dict[current_row].append(current_items_col)

        current_row += 1

    f.close()

    # print(none_zeros)
    # print(len(none_zeros))
    # nnz_dict = dict(none_zeros)
    # print(nnz_dict)
    print(len(nnz_dict))
    return nnz_dict

def cal_nnz_entries(nnz_dict):
    num = 0
    for key, value in nnz_dict.items():
        num += len(value)

    print(num)
    return num

def save_dict2txt(row_col_file, col_row_file, rows, cols, nnzs, nnz_dict):
    # 按 row col 形式保存校验矩阵 H
    f1 = open(row_col_file, 'w')
    f1.write("%d %d %d\n" % (rows, cols, nnzs))
    for key, value in nnz_dict.items():
        for col_index in value:
            f1.write("%d %d\n" % (key, col_index))
    f1.close()


def matrix2dictionary_two_dicts(filename):
    f = open(filename, 'rb')
    first_4bytes = f.read(4)
    first_num = int.from_bytes(first_4bytes, byteorder='big', signed=True)
    print(first_num)

    second_4bytes = f.read(4)
    # second_num: 最后一个有效4字节, 下一个4字节为'0xFF FF FF FF'
    second_num = int.from_bytes(second_4bytes, byteorder='big', signed=True)
    print(second_num)

    valid_items = second_num - 1
    # valid_items = 63 - 1
    i = 0
    current_row = 0
    none_zeros = []
    while i < valid_items:
        current_row_items_4bytes = f.read(4)
        current_row_items = int.from_bytes(current_row_items_4bytes, byteorder='big', signed=True)
        i += 1

        for j in range(current_row_items):
            current_items_col_4bytes = f.read(4)
            current_items_col = int.from_bytes(current_items_col_4bytes, byteorder='big', signed=True)
            i += 1

            none_zeros.append((current_row, current_items_col))

        current_row += 1

    f.close()

    # print(none_zeros)
    # print(len(none_zeros))

    nnz_dict_rc = defaultdict(list)
    nnz_dict_cr = defaultdict(list)
    for k, v in none_zeros:
        nnz_dict_rc[k].append(v)
        nnz_dict_cr[v].append(k)

    # print(nnz_dict_rc)
    # print(len(nnz_dict_rc))
    #
    # print(nnz_dict_cr)
    # print(len(nnz_dict_cr))

    return nnz_dict_rc, nnz_dict_cr


if __name__ == '__main__':
    # H_matrix_file = 'H_80_100000.bin'
    # nnz_dict = matrix2dictionary(H_matrix_file)
    #
    # # d = dict.fromkeys(range(2), [])
    # # print(d)
    # # d[2] = []
    # # print(d)
    #
    # row_col_txt = 'row_col_80_100000.txt'
    # col_row_txt = 'col_row_80_100000.txt'
    #
    # num_nnz_entries = cal_nnz_entries(nnz_dict)
    # num_row_check_node = len(nnz_dict)
    # num_col_variable_node = 100000

    H_matrix_file = 'H_80_100000.bin'
    rc, cr = matrix2dictionary_two_dicts(H_matrix_file)
    row_col_txt = 'row_col_80_100000.txt'
    col_row_txt = 'col_row_80_100000.txt'

    num_nnz_entries = cal_nnz_entries(rc)
    num_row_check_node = len(rc)
    num_col_variable_node = 100000




