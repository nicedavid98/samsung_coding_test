from collections import deque

dr = [-1,0,1,0]  #북동남서
dc = [0,1,0,-1]


# 전역변수
gollems = []  # [r, c, dir, 살아있는지], 모든 골렘 모음, 죽은 골렘도 있을 수 있음
answer = 0

# 입력부
R, C, K = map(int, input().split())



def print_visited(visited):
    for row in visited:
        print(row)
    print()


def print_board(board):
    for row in board:
        print(row)
    print()


# 맵을 그려주는 함수, 살아있는 골렘만 그린다
def make_board():
    board = [[0 for _ in range(C)] for _ in range(R + 3)]
    for nidx in range(len(gollems)):
        next_r, next_c, next_exit, next_alive = gollems[nidx]
        if not next_alive:  # 죽은 골렘은 패쓰
            continue
        pos = gollem_pos(nidx)  # 현재 순회중인 골렘이 차지하는 좌표들
        for r, c in pos:
            board[r][c] = nidx
        board[next_r + dr[next_exit]][next_c + dc[next_exit]] = -1 * nidx  # 출구는 -1을 곱해서 처리
    return board


# 골렘이 차지하는 좌표들의 리스트 반환
def gollem_pos(gidx):
    curr_r, curr_c, curr_exit, is_alive = gollems[gidx]
    return [[curr_r, curr_c], [curr_r+1, curr_c], [curr_r-1, curr_c], [curr_r, curr_c-1], [curr_r, curr_c+1]]


# 해당 골렘이 차지하는 좌표들이 격자 안인지 check
def is_inside(gidx):
    pos = gollem_pos(gidx)
    for r, c in pos:
        if not (3 <= r <= R+2 and 0 <= c <= C-1):  # 하나라도 격자 밖이면
            return False
    return True


# 아래로 내려갈 수 있는가?
# 가능하면, 이동 처리 + True
def move_south(curr_idx):
    curr_r, curr_c, curr_exit, is_alive = gollems[gidx]
    next_pos = [[curr_r+1, curr_c-1], [curr_r+2, curr_c], [curr_r+1, curr_c+1]]  # 이동을 위해 비어있어야 하는 좌표들 모음

    # 이동 후, 하나라도 격자 밖이면
    for r, c in next_pos:
        if not (0 <= r <= R + 2 and 0 <= c <= C - 1):
            return False

    # 모든 골렘 순회 (자신은 제외 혹시나 ㅎㅎ)
    for nidx in range(len(gollems)):
        if gollems[nidx][3] == False:  # 죽은 골렘은 패쓰
            continue
        nidx_gollem_pos = gollem_pos(nidx)  # 현재 순회중인 골렘이 차지하는 좌표들
        for pos in next_pos:
            if pos in nidx_gollem_pos:  # 이동 후 좌표에, 다른 골렘이 존재하면
                return False

    # 여기까지 왔으면 움직일 수 있음
    # 이동처리
    gollems[curr_idx][0] += dr[2]
    gollems[curr_idx][1] += dc[2]

    return True


# 서쪽으로 갈 수 있는가?
# 가능하면, 이동 처리 + True
def move_west(curr_idx):
    curr_r, curr_c, curr_exit, is_alive = gollems[gidx]
    next_pos = [[curr_r-1, curr_c-1], [curr_r, curr_c-2], [curr_r+1, curr_c-2],
                [curr_r+1, curr_c-1], [curr_r+2, curr_c-1]]  # 이동을 위해 비어있어야 하는 좌표들 모음

    # 이동 후, 하나라도 격자 밖이면
    for r, c in next_pos:
        if not (0 <= r <= R + 2 and 0 <= c <= C - 1):
            return False

    # 모든 골렘 순회 (자신은 제외 혹시나 ㅎㅎ)
    for nidx in range(len(gollems)):
        if gollems[nidx][3] == False:  # 죽은 골렘은 패쓰
            continue
        nidx_gollem_pos = gollem_pos(nidx)  # 현재 순회중인 골렘이 차지하는 좌표들
        for pos in next_pos:
            if pos in nidx_gollem_pos:  # 이동 후 좌표에, 다른 골렘이 존재하면
                return False

    # 여기까지 왔으면 움직일 수 있음
    # 이동처리
    gollems[curr_idx][0] += (dr[3] + dr[2])
    gollems[curr_idx][1] += (dc[3] + dc[2])
    gollems[curr_idx][2] = abs(curr_exit + 3) % 4

    return True


# 동쪽으로 갈 수 있는가?
# 가능하면, 이동 처리 + True
def move_east(curr_idx):
    curr_r, curr_c, curr_exit, is_alive = gollems[gidx]
    next_pos = [[curr_r-1, curr_c+1], [curr_r, curr_c+2], [curr_r+1, curr_c+2],
                [curr_r+1, curr_c+1], [curr_r+2, curr_c+1]]  # 이동을 위해 비어있어야 하는 좌표들 모음

    # 이동 후, 하나라도 격자 밖이면
    for r, c in next_pos:
        if not (0 <= r <= R + 2 and 0 <= c <= C - 1):
            return False

    # 모든 골렘 순회
    for nidx in range(len(gollems)):
        if gollems[nidx][3] == False:  # 죽은 골렘은 패쓰
            continue
        nidx_gollem_pos = gollem_pos(nidx)  # 현재 순회중인 골렘이 차지하는 좌표들
        for pos in next_pos:
            if pos in nidx_gollem_pos:  # 이동 후 좌표에, 다른 골렘이 존재하면
                return False

    # 여기까지 왔으면 움직일 수 있음
    # 이동처리
    gollems[curr_idx][0] += (dr[1] + dr[2])
    gollems[curr_idx][1] += (dc[1] + dc[2])
    gollems[curr_idx][2] = (curr_exit + 1) % 4

    return True


# 아래 => 서쪽 => 동쪽 모두 다 움직일 수 없으면 False 반환
def move(curr_idx):
    if not move_south(curr_idx):
        if not move_west(curr_idx):
            if not move_east(curr_idx):
                return False
    return True


def BFS(visited, start_r, start_c):
    q = deque()
    q.append([start_r, start_c])
    visited[start_r][start_c] = 1
    while q:
        cr, cc = q.popleft()
        for dir in range(4):
            nr = cr + dr[dir]
            nc = cc + dc[dir]

            # 공통 : 격자 밖이거나, 이미 방문했거나, 골렘 안이 아니면 패쓰
            if not (3<=nr<=R+2 and 0<=nc<=C-1) or visited[nr][nc] or board[nr][nc] == 0:
                continue

            # 현재 출구인지 아닌지 경우로 나누어 생각
            if board[cr][cc] < 0:  # 출구이면
                q.append([nr, nc])
                visited[nr][nc] = 1
            elif board[cr][cc] > 0:  # 골렘 안이지만, 출구가 아니면
                if board[nr][nc] == board[cr][cc] or board[nr][nc] == -1 * board[cr][cc]:
                    q.append([nr, nc])
                    visited[nr][nc] = 1


def calculate_score(visited):
    for i in range(R + 2, -1, -1):
        for j in range(C):
            if visited[i][j] == 1:
                return i - 2


# 메인 루프
gollems.append([-1,-1,-1, False])  # 유효한 골렘 인덱스는 (1~K)
for gidx in range(1, K+1):
    c, d = map(int, input().split())
    c -= 1  # 좌표처리

    # 골렘 입구에 넣어주기
    gollems.append([1, c, d, True])

    # 이동 처리
    while True:
        if not move(gidx):
            break

    # 다들 격자 안이면 점수 계산
    board = make_board()  # 실제 맵은 row idx 기준 (3 ~ R+2), (0~2)까지는 격자 밖으로 취급
    visited = [[0 for _ in range(C)] for _ in range(R + 3)]

    # print("=============================col: ", c)
    # print_board(board)

    # 만약 격자를 벗어난 골렘이 있으면, 기존 골렘들 다 죽여버려
    if not is_inside(gidx):
        for nidx in range(len(gollems)):
            gollems[nidx][3] = False

    else:
        # BFS로 점수계산
        BFS(visited, gollems[gidx][0], gollems[gidx][1])
        temp_answer = calculate_score(visited)
        answer += temp_answer

    # print_visited(visited)
    # print()


print(answer)