from copy import deepcopy
from collections import deque

dr = [0,0,-1,1]
dc = [-1,1,0,0]

K, M = map(int, input().split())
board = []  # 보드
cracks = []  # 유물 조각
cracks_idx = 0  # 다음 채워 넣을 cracks 인덱스 값

for _ in range(5):
    row = list(map(int, input().split()))
    board.append(row)
cracks = list(map(int, input().split()))


# 배열 회전 함수
def rotate(grid, start_row, end_row, start_col, end_col):
    subgrid = [row[start_col:end_col+1] for row in grid[start_row:end_row+1]]
    rotated_subgrid = list(zip(*subgrid[::-1]))
    for i in range(start_row, end_row+1):
        for j in range(start_col, end_col+1):
            grid[i][j] = rotated_subgrid[i - start_row][j - start_col]


# return 값은 해당 덩어리의 크기!
def BFS(board, visited, start_row, start_col):
    crack_num = board[start_row][start_col]
    q = deque()
    visited[start_row][start_col] = 1
    q.append([start_row, start_col])
    size = 0  # 덩어리 크기
    while q:
        curr_r, curr_c = q.popleft()
        size += 1
        for dir in range(4):
            nr = curr_r + dr[dir]
            nc = curr_c + dc[dir]
            if 0 <= nr <= 4 and 0 <= nc <= 4:  # 격자 안이면
                if visited[nr][nc] == 0 and board[nr][nc] == crack_num:  # 방문 X, 같은 조각 번호일 경우
                    visited[nr][nc] = visited[curr_r][curr_c] + 1
                    q.append([nr, nc])
    return size


# 덩어리 크기가 3 이상인 경우, visited에 -1을 박아놓는 함수
def bfs_mark(board, visited, start_row, start_col):
    crack_num = board[start_row][start_col]
    q = deque()
    visited[start_row][start_col] = -1
    q.append([start_row, start_col])
    size = 0  # 덩어리 크기
    while q:
        curr_r, curr_c = q.popleft()
        size += 1
        for dir in range(4):
            nr = curr_r + dr[dir]
            nc = curr_c + dc[dir]
            if 0 <= nr <= 4 and 0 <= nc <= 4:  # 격자 안이면
                if visited[nr][nc] == 0 and board[nr][nc] == crack_num:  # 방문 X, 같은 조각 번호일 경우
                    visited[nr][nc] = -1
                    q.append([nr, nc])
    return size


# 격자를 모두 돌면서, 최적의 탐사를 찾아 반환. [1차 가치, 회전 각도, 중심 열, 중심 행]
def explore():
    record = []  # 회전 정보를 기록하는 배열 [-1 * 1차 가치, 회전 각도, 중심 열, 중심 행]

    # 중심을 바꾸어가며 회전시키기
    for rotate_row in range(0, 3):
        for rotate_col in range(0, 3):
            for rotate_cnt in range(1, 4):  # 회전 횟수 (90, 180, 270)
                visited = [[0, 0, 0, 0, 0] for _ in range(5)]
                board_copy = deepcopy(board)
                for _ in range(rotate_cnt):
                    rotate(board_copy, rotate_row, rotate_row+2, rotate_col, rotate_col+2)

                # 격자를 회전시킨 후!
                score_sum = 0
                for r in range(5):
                    for c in range(5):
                        if visited[r][c] == 0:
                            size = BFS(board_copy, visited, r, c)
                            if size >= 3:
                                score_sum += size

                # 결과값을 기록
                record.append([-score_sum, rotate_cnt, rotate_col, rotate_row])
    record.sort()
    for rec in record:
        rec[0] = rec[0] * -1

    return record[0]


# 새로운 조각을 채워넣을 곳에 -1을 마크함
def mark(mark_visited):
    visited = [[0, 0, 0, 0, 0] for _ in range(5)]
    for r in range(5):
        for c in range(5):
            if visited[r][c] == 0:
                size = BFS(board, visited, r, c)
                if size >= 3:
                    bfs_mark(board, mark_visited, r, c)


# mark_visited 를 보고 채우기
def fill(mark_visited):
    global cracks_idx, board
    for c in range(5):
        for r in range(4, -1, -1):
            if mark_visited[r][c] == -1:
                board[r][c] = cracks[cracks_idx]
                cracks_idx += 1  # cracks 인덱스 전역변수 ++


# 유물 연쇄 획득의 한 턴을 의미하는 함수, 얻을 수 있는 점수를 출력
def chain_iter(board):
    visited = [[0, 0, 0, 0, 0] for _ in range(5)]
    score_sum = 0
    for r in range(5):
        for c in range(5):
            if visited[r][c] == 0:
                size = BFS(board, visited, r, c)
                if size >= 3:
                    score_sum += size

    # 더 이상 얻을 점수가 없다면 종료
    if score_sum <= 0:
        return 0

    # 새로운 조각을 채워넣을 곳에 -1을 마크함
    mark_visited = [[0, 0, 0, 0, 0] for _ in range(5)]
    mark(mark_visited)

    fill(mark_visited)

    return score_sum


# 한 turn
def turn():
    global board

    # 탐사 후 최적 조건 찾기
    score, rotate_cnt, rotate_col, rotate_row = explore()

    # 탐사 과정에서 유물 획득 못한 경우 즉시 종료.
    if score == 0:
        return 0

    # 진짜 회전 실행.
    for _ in range(rotate_cnt):
        rotate(board, rotate_row, rotate_row + 2, rotate_col, rotate_col + 2)

    # 새로운 조각을 채워넣을 곳에 -1을 마크함
    mark_visited = [[0, 0, 0, 0, 0] for _ in range(5)]
    mark(mark_visited)

    # 채우기
    fill(mark_visited)

    # 유물 연쇄 획득
    while True:
        sub_score = chain_iter(board)
        if sub_score <= 0:
            break
        else:
            score += sub_score

    return score


# 메인 함수 : 총 k개의 턴 만큼 진행
for _ in range(K):
    ret = turn()
    if ret == 0:
        break
    else:
        print(ret, end=" ")


