
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
    nnz_c = sorted(nnz, key=lambda x :(x[1], x[0]))
    f1 = open(col_row_file, 'w')
    f1.write("%d %d %d\n" % (rows, cols, nnzs))
    for row_index, col_index in nnz_c:
        f1.write("%d %d\n" % (row_index, col_index))
    f1.close()

if __name__ == '__main__':
    H_matrix_file = 'H_80_100000.bin'
    nnz = matrix2dictionary_tuple(H_matrix_file)
    row_col_txt = 'row(base)_col_80_100000.txt'
    col_row_txt = 'row_col(base)_80_100000.txt'
    save_dict2txt_tuple(row_col_txt, col_row_txt, nnz)
