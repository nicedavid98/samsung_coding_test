
def rotate(grid, start_r, start_c, end_r, end_c):
    subgrid = [row[start_c:end_c+1] for row in grid[start_r:end_r+1]]
    rotated_subgrid = list(zip(*subgrid[::-1]))
    for i in range(start_r, end_r+1):
        for j in range(start_c, end_c+1):
            grid[i][j] = rotated_subgrid[i-start_r][j-start_c]


test_arr = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]

for row in test_arr:
    print(row)
print()

rotate(test_arr, 1,1,3,3)

for row in test_arr:
    print(row)