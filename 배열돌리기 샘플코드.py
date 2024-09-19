
def rotate_subgrid_clockwise(grid, start_row, start_col, end_row, end_col):
    subgrid = [row[start_col:end_col+1] for row in grid[start_row:end_row+1]]
    rotated_subgrid = list(zip(*subgrid[::-1]))  # 시계 방향 회전
    for i in range(start_row, end_row+1):
        for j in range(start_col, end_col+1):
            grid[i][j] = rotated_subgrid[i-start_row][j-start_col]

def rotate_subgrid_counterclockwise(grid, start_row, start_col, end_row, end_col):
    subgrid = [row[start_col:end_col+1] for row in grid[start_row:end_row+1]]
    rotated_subgrid = list(zip(*subgrid))[::-1]  # 반시계 방향 회전
    for i in range(start_row, end_row+1):
        for j in range(start_col, end_col+1):
            grid[i][j] = rotated_subgrid[i-start_row][j-start_col]


# 격자 생성 및 초기화
grid = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]


print("Original Grid:")
for row in grid:
    print(row)

# 시계 방향으로 부분 격자 회전 테스트
print("\nRotating subgrid clockwise:")
rotate_subgrid_clockwise(grid, 0, 0, 2, 2)
for row in grid:
    print(row)

# 반시계 방향으로 부분 격자 회전 테스트
print("\nRotating subgrid counterclockwise:")
rotate_subgrid_counterclockwise(grid, 1, 1, 2, 2)
for row in grid:
    print(row)



