

# arr = [0,1,2,3]
#
# # 중복 순열
# def product(length, new_arr):
#     if len(new_arr) == length:
#         print(new_arr)
#         return
#     for i in range(0 ,len(arr)):
#         product(length, new_arr + [arr[i]])
#
# product(3, [])
#
#
# # for dir in range(2, 8):
# #     print(dir)
# # for dir in range(0, 2):
# #     print(dir)


def rotate_subgrid_clockwise(grid, start_row, start_col, end_row, end_col):
    subgrid = [row[start_col:end_col+1] for row in grid[start_row:end_row+1]]
    rotated_subgrid = list(zip(*subgrid[::-1]))
    for i in range(start_row, end_row+1):
        for j in range(start_col, end_col+1):
            grid[i][j] = rotated_subgrid[i-start_row][j-start_col]