from collections import deque

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

R, C, K = map(int, input().split())

board = [[0 for _ in range(C)] for _ in range(R + 3)]  # row 0-2은 바깥임.
gollems = []  # [id, 중심좌표 R, 중심좌표 C, 출구 방향(0-3)]

gollems.append([0,0,0,0])
for id in range(K):
    c, d = map(int, input().split())
    gollems.append([id+1, 0, c-1, d])  # 격자는 가장 위를 1행이므로 미리 0행으로 반환하여 저장.


def turn_clock(dir):
    nd = (dir + 1) % 4
    return nd


def turn_counter_clock(dir):
    nd = (dir - 1)
    if nd == -1:
        nd = 3
    return nd


def find_exit(r, c, d):
    nr = r + dr[d]
    nc = c + dc[d]
    return [nr, nc]


def move_south(gollem_idx):
    id, r, c, d = gollems[gollem_idx]
    nrs = [r + 1, r + 2, r + 1]
    ncs = [c - 1, c, c + 1]

    can_move = True
    for i in range(3):
        nr = nrs[i]
        nc = ncs[i]
        if not (0 <= nr <= R + 2 and 0 <= nc <= C - 1 and board[nr][nc] == 0):
            can_move = False

    if can_move:
        gollems[gollem_idx] = [id, r+1, c, d]
        return True
    else:
        return False


def move_west(gollem_idx):
    id, r, c, d = gollems[gollem_idx]
    nrs = [r-1, r, r+1, r+1, r+2]
    ncs = [c-1, c-2, c-2, c-1, c-1]

    can_move = True
    for i in range(5):
        nr = nrs[i]
        nc = ncs[i]
        if not (0 <= nr <= R + 2 and 0 <= nc <= C - 1 and board[nr][nc] == 0):
            can_move = False

    if can_move:
        nd = turn_counter_clock(d)
        gollems[gollem_idx] = [id, r+1, c-1, nd]
        return True
    else:
        return False


def move_east(gollem_idx):
    id, r, c, d = gollems[gollem_idx]
    nrs = [r-1, r, r+1, r+1, r+2]
    ncs = [c+1, c+2, c+2, c+1, c+1]

    can_move = True
    for i in range(5):
        nr = nrs[i]
        nc = ncs[i]
        if not (0 <= nr <= R + 2 and 0 <= nc <= C - 1 and board[nr][nc] == 0):
            can_move = False

    if can_move:
        nd = turn_clock(d)
        gollems[gollem_idx] = [id, r+1, c+1, nd]
        return True
    else:
        return False

# 우선 남쪽, 그게 안되면 서쪽, 그게 안되면 동쪽, 그게 안되면 False 반환
# 즉, 한번의 움직임을 표현한 함수
def move_once(gollem_idx):
    if move_south(gollem_idx):
        return True
    if move_west(gollem_idx):
        return True
    if move_east(gollem_idx):
        return True

    return False


# move_once를 여러번 호출하여 골렘을 끝까지 움직이고, 맵에 기록하는 함수
def move(gollem_idx):
    global board

    # 더 이상 움직일 수 없을 때 까지 move_once 를 계속 호출
    while True:
        movable = move_once(gollem_idx)
        if not movable:
            break

    id, r, c, d = gollems[gollem_idx]

    #  골렘의 몸 일부가 여전히 숲을 벗어난 상태
    if not (4 <= r <= R+2 and 0 <= c <= C-1):
        board = [[0 for _ in range(C)] for _ in range(R + 3)]  # 보드 초기화.
        return False
    # 그렇지 않으면, 맵에 기록하기
    else:
        board[r][c] = id
        for k in range(4):
            nr = r + dr[k]
            nc = c + dc[k]
            board[nr][nc] = id
        exit_r, exit_c = find_exit(r, c, d)
        board[exit_r][exit_c] = -1 * id  # 출구는 음수로 기록.
        return True


# 골렘이 다 움직인 후, 정령을 움직이는 함수
def bfs(visited, gollem_idx):
    id, r, c, d = gollems[gollem_idx]
    q = deque()
    visited[r][c] = 1
    q.append([r, c])
    while q:
        cr, cc = q.popleft()
        for k in range(4):
            nr = cr + dr[k]
            nc = cc + dc[k]
            # inqueue 조건 1 : 범위 침범 X and 방문 X
            if 0 <= nr <= R + 2 and 0 <= nc <= C - 1 and visited[nr][nc] == 0:
                # inqueue 조건 2 : 다음 좌표가 같은 덩어리 안이거나 (board[nr][nc] == board[cr][cc] or board[nr][nc] == -1 * board[cr][cc]), 현재 좌표가 포털이고 다음 좌표에 덩어리가 존재할 때 (board[cr][cc] < 0 and board[nr][nc] != 0)
                # cf) 사실 이렇게 포털을 -id로 표현한 건 좋은 방법이 아닌 듯함. 그냥 포털들의 목록을 배열로 만들어 포털인지 아닌지 판단하게 해주면 더 좋지 않았을까..
                if board[nr][nc] == board[cr][cc] or board[nr][nc] == -1 * board[cr][cc] or (board[cr][cc] < 0 and board[nr][nc] != 0):
                    q.append([nr, nc])
                    visited[nr][nc] = 1


# 정령이 어디까지 갔는지 점수를 확인하는 함수
def get_score(visited):
    for r in range(R+2, -1, -1):
        for c in range(C):
            if visited[r][c] == 1:
                return r - 2


# 정령이 한 번 들어왔을 때를 처리하는 단위의 함수, 총 K번 호출될 예정.
def iteration(gollem_idx):
    if not move(gollem_idx):
        return 0
    visited = [[0 for _ in range(C)] for _ in range(R + 3)]
    bfs(visited, gollem_idx)
    return get_score(visited)


# 메인 함수
answer = 0
for i in range(1, K+1):
    ret = iteration(i)
    answer += ret
print(answer)


# 배운 점
'''
1. BFS 새로운 제약사항 처리 방법 : 특정 덩어리에서 다른 덩어리로 넘어가는 포털? 사용 방법
2. 지역변수 shadow 주의하기.. 이번 문제에서는 dr, dc 순회를 위한 for d in range(4)가 앞의 d를 가려버리는 일 발생.. 
   => 앞으로는 dr, dc 순회를 위해 가급적으로 for k in range(4)를 사용하기로. 
'''


















