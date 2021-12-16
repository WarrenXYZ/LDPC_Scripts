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
    print("*" * 10)
    s = b'\xff\xff\xff\xff'
    print(int.from_bytes(s, byteorder='big', signed=False))
    print(int.from_bytes(s, byteorder='big'))  # 默认无符号
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

    # print(num)
    return num


def save_dict2txt(row_col_file, col_row_file, nnz_dict_rc, nnz_dict_cr):
    nnzs = cal_nnz_entries(nnz_dict_rc)
    rows = len(nnz_dict_rc)
    cols = len(nnz_dict_cr)
    # 按 row col 形式保存校验矩阵 H
    # e.g.  0 0\n
    #       0 1\n
    #       ...
    f0 = open(row_col_file, 'w')
    f0.write("%d %d %d\n" % (rows, cols, nnzs))
    for key, value in nnz_dict_rc.items():
        for col_index in value:
            f0.write("%d %d\n" % (key, col_index))
    f0.close()

    # 按 col row 形式保存校验矩阵 H
    # 实际仍是 row col 形式
    # e.g.  0 0\n
    #       1 0\n
    #       ...
    f1 = open(col_row_file, 'w')
    f1.write("%d %d %d\n" % (rows, cols, nnzs))
    for key, value in nnz_dict_cr.items():
        for row_index in value:
            f1.write("%d %d\n" % (row_index, key))
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

def matrix2dictionary_tuple(filename):
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

    return none_zeros

def save_dict2txt_tuple(row_col_file, col_row_file, nnz):
    nnzs = 589940
    rows = 2000
    cols = 100000
    # TODO: 通过 nnz 统计 rows, cols, nnzs
    # 按 row col 形式保存校验矩阵 H
    # e.g.  0 0\n
    #       0 1\n
    #       ...
    nnz_r = nnz # 无需排序
    f0 = open(row_col_file, 'w')
    f0.write("%d %d %d\n" % (rows, cols, nnzs))
    for row_index, col_index in nnz_r:
        f0.write("%d %d\n" % (row_index, col_index))
    f0.close()

    # 按 col row 形式保存校验矩阵 H
    # 实际仍是 row col 形式
    # e.g.  0 0\n
    #       1 0\n
    #       ...
    nnz_c = sorted(nnz, key=lambda x:(x[1], x[0]))
    f1 = open(col_row_file, 'w')
    f1.write("%d %d %d\n" % (rows, cols, nnzs))
    for row_index, col_index in nnz_c:
        f1.write("%d %d\n" % (row_index, col_index))
    f1.close()

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

    # H_matrix_file = 'H_80_100000.bin'
    # rc, cr = matrix2dictionary_two_dicts(H_matrix_file)
    # print(sorted(cr))
    # row_col_txt = 'row(base)_col_80_100000.txt'
    # col_row_txt = 'row_col(base)_80_100000.txt'

    # num_nnz_entries = cal_nnz_entries(rc)   # == cal_nnz_entries(cr)
    # num_row_check_node = len(rc)
    # num_col_variable_node = len(cr)

    # TODO: rc, cr 未按键值排序
    # save_dict2txt(row_col_txt, col_row_txt, rc, cr)

    H_matrix_file = 'H_80_100000.bin'
    nnz = matrix2dictionary_tuple(H_matrix_file)
    row_col_txt = 'row(base)_col_80_100000.txt'
    col_row_txt = 'row_col(base)_80_100000.txt'
    save_dict2txt_tuple(row_col_txt, col_row_txt, nnz)