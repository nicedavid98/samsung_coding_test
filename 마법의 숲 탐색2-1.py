from collections import deque


dr = [-1,0,1,0]  #북동남서
dc = [0,1,0,-1]


# 전역변수
gollems = []  # [r, c, dir, 살아있는지], 모든 골렘 모음, 죽은 골렘도 있을 수 있음
board = []
answer = 0

# 입력부
R, C, K = map(int, input().split())
board = [[0 for _ in range(C)] for _ in range(R + 3)]


def print_visited(visited):
    for row in visited:
        print(row)
    print()


def print_board():
    for row in board:
        print(row)
    print()


# 배열에 있던 골렘들을 board에 그려줌, 살아있는 골렘만 그린다
def make_board():
    global board
    board = [[0 for _ in range(C)] for _ in range(R + 3)]
    for nidx in range(len(gollems)):
        next_r, next_c, next_exit, next_alive = gollems[nidx]
        if not next_alive:  # 죽은 골렘은 패쓰
            continue
        pos = gollem_pos(nidx)  # 현재 순회중인 골렘이 차지하는 좌표들
        for r, c in pos:
            board[r][c] = nidx
        board[next_r + dr[next_exit]][next_c + dc[next_exit]] = -1 * nidx  # 출구는 -1을 곱해서 처리


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
# 가능하면, 배열에서만 이동 처리 + True
def move_south(curr_idx):
    curr_r, curr_c, curr_exit, is_alive = gollems[gidx]
    next_pos = [[curr_r+1, curr_c-1], [curr_r+2, curr_c], [curr_r+1, curr_c+1]]  # 이동을 위해 비어있어야 하는 좌표들 모음

    for r, c in next_pos:
        if not (0 <= r <= R + 2 and 0 <= c <= C - 1):  # 이동 후, 하나라도 격자 밖이면
            return False
        if board[r][c] != 0:  # 이동 후, 하나라도 다른 정령과 겹치면
            return False

    # 여기까지 왔으면 움직일 수 있음
    # 이동처리
    gollems[curr_idx][0] += dr[2]
    gollems[curr_idx][1] += dc[2]

    return True


# 서쪽으로 갈 수 있는가?
# 가능하면, 배열에서만 이동 처리 + True
def move_west(curr_idx):
    curr_r, curr_c, curr_exit, is_alive = gollems[gidx]
    next_pos = [[curr_r-1, curr_c-1], [curr_r, curr_c-2], [curr_r+1, curr_c-2],
                [curr_r+1, curr_c-1], [curr_r+2, curr_c-1]]  # 이동을 위해 비어있어야 하는 좌표들 모음

    for r, c in next_pos:
        if not (0 <= r <= R + 2 and 0 <= c <= C - 1):  # 이동 후, 하나라도 격자 밖이면
            return False
        if board[r][c] != 0:  # 이동 후, 하나라도 다른 정령과 겹치면
            return False

    # 여기까지 왔으면 움직일 수 있음
    # 이동처리
    gollems[curr_idx][0] += (dr[3] + dr[2])
    gollems[curr_idx][1] += (dc[3] + dc[2])
    gollems[curr_idx][2] = abs(curr_exit + 3) % 4

    return True


# 동쪽으로 갈 수 있는가?
# 가능하면, 배열에서만 이동 처리 + True
def move_east(curr_idx):
    curr_r, curr_c, curr_exit, is_alive = gollems[gidx]
    next_pos = [[curr_r-1, curr_c+1], [curr_r, curr_c+2], [curr_r+1, curr_c+2],
                [curr_r+1, curr_c+1], [curr_r+2, curr_c+1]]  # 이동을 위해 비어있어야 하는 좌표들 모음

    for r, c in next_pos:
        if not (0 <= r <= R + 2 and 0 <= c <= C - 1):  # 이동 후, 하나라도 격자 밖이면
            return False
        if board[r][c] != 0:  # 이동 후, 하나라도 다른 정령과 겹치면
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

    # 이동 처리 (배열에서만)
    while True:
        if not move(gidx):
            break

    # 1. 만약 격자를 벗어나면, 기존 골렘들 다 죽여버려
    if not is_inside(gidx):
        for nidx in range(len(gollems)):
            gollems[nidx][3] = False
        make_board()  # 죽이고 나서 board에도 반영해줘야함
        continue

    # 2. 격자 안에 잘 들어온 경우
    # 움직일 수 있는 경우, 배열에 관리되었던 정령들을 격자에 적용
    make_board()
    # print_board()

    # BFS로 점수계산
    visited = [[0 for _ in range(C)] for _ in range(R + 3)]
    BFS(visited, gollems[gidx][0], gollems[gidx][1])
    temp_answer = calculate_score(visited)
    answer += temp_answer
    # print_visited(visited)


print(answer)


"""
느낀점 :
1. for i in range(N,-1, -1) => (N~0) 순회 

2. 덩어리 문제라 무조건 격자가 아닌 배열로 관리하려함. 로직상으로는 틀리지 않았지만 시간복잡도 이슈로 시간초과를 받음 
=> 정령의 개수가 1000개까지였음. 1000개면 시간복잡도를 어느정도는 신경써야 할듯 

3. 역방향 주의 !!!
abs(dir-1) % 4 했는데... 이러면 원래 0이었을때 안되자나요 
=> (dir+3) % 4 를 생활화 하자.  

4. (2)번과 비슷한 맥락이긴 한데, 처음 문제를 보고 정렬의 개수 1000개를 보고 살짝 쎄함을 느꼈어야.
=> 그 후 자료구조를 고민할 때, 격자를 사용하는 방안을 생각했어야. 왜냐면, 그렇게 안하면 정렬과 겹치는 것을 확인하기 위해서는 1000개씩 다 순회해야 하기 때문 
=> 구현을 할 때는 항상. 배열과 격자를 어느 타이밍에 적절히 업데이트 시켜줄 것인가에 대한 고민을 열심히 하여야 함. 사실 구현 시작하기 전에 먼저 구상하고 들어가야 함

5. 자료구조 고민할 때, 최종 점수를 어떻게 내야하는지도 잘 보고 들어가야함. 
=> 골렘 자료구조에 생존여부도 저장했어야 하는데, 그걸 까먹었음 .. ^^ 그림이랑 문제 이해했다고 너무 신나게 들어가지는 말자.
"""
