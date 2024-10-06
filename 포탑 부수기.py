from collections import deque
from copy import deepcopy

N, M, K = map(int, input().split())

board = []
attack_record = [[0 for _ in range(M)] for _ in range(N)]  # 어느 턴에 공격하였는지 기록하는 이차원 배열 (한번도 공격하지 않은 포탑은 0, 따라서 turn은 1부터 시작해야)

for _ in range(N):
    temp_row = list(map(int, input().split()))
    board.append(temp_row)


# 공격자의 좌표를 리턴
def select_attacker(turn):
    min_attack_stat = 10000  # 최소 공격력 찾기 (0은 부서진 포탑이므로 제외해야)
    for i in range(N):
        for j in range(M):
            if min_attack_stat > board[i][j] and board[i][j] != 0:
                min_attack_stat = board[i][j]

    cand = []  # 공격력이 최소인 포탑들
    for i in range(N):
        for j in range(M):
            if board[i][j] == min_attack_stat:
                cand.append([-1 * attack_record[i][j], -1 * (i+j), -1 * j, [i, j]])

    if cand:
        cand.sort()

    # 선정된 공격자의 좌표
    attacker_r, attacker_c = cand[0][-1]

    # 공격자로 선정된 포탑을 attack_record 에 기록
    attack_record[attacker_r][attacker_c] = turn

    # 공격자로 선정되면 공격력 버프를 얻음
    board[attacker_r][attacker_c] = board[attacker_r][attacker_c] + N + M

    return [attacker_r, attacker_c]


# 공격자 대상자의 좌표를 리턴
def select_target(attacker_r, attacker_c):
    max_attack_stat = -1  # 최대 공격력 찾기
    for i in range(N):
        for j in range(M):
            if max_attack_stat < board[i][j] and not (i == attacker_r and j == attacker_c):  # 자기 자신은 제외해야
                max_attack_stat = board[i][j]

    cand = []  # 공격력이 최대인 포탑들
    for i in range(N):
        for j in range(M):
            if board[i][j] == max_attack_stat and not (i == attacker_r and j == attacker_c):  # 자기 자신은 제외해야
                cand.append([attack_record[i][j], i + j, j, [i, j]])

    if cand:
        cand.sort()

    # 선정된 공격 대상자의 좌표
    target_r, target_c = cand[0][-1]

    return [target_r, target_c]


def move(row, col, dir):
    dr = [0, 1, 0, -1, 1, 1, -1, -1]
    dc = [1, 0, -1, 0, 1, -1, 1, -1]  # 우 하 좌 상

    nr = row + dr[dir]
    nc = col + dc[dir]

    if nr == -1:
        nr = N-1
    elif nr == N:
        nr = 0

    if nc == -1:
        nc = M-1
    elif nc == M:
        nc = 0

    return [nr, nc]


# 레이저 공격 성공 여부 리턴
def laser_attack(attacker_r, attacker_c, target_r, target_c):

    visited = [[0 for _ in range(M)] for _ in range(N)]
    directions_2D = [[[] for _ in range(M)] for _ in range(N)]  # 이동방향을 저장한 2차원 배열

    # BFS 로직 시작
    q = deque()
    q.append([attacker_r, attacker_c])
    visited[attacker_r][attacker_c] = 1

    while q:
        cr, cc = q.popleft()
        for d in range(4):
            nr, nc = move(cr, cc, d)
            if visited[nr][nc] == 0 and board[nr][nc] != 0:
                visited[nr][nc] = visited[cr][cc] + 1
                directions_2D[nr][nc] = deepcopy(directions_2D[cr][cc])
                directions_2D[nr][nc].append(d)
                q.append([nr, nc])

    # 공격 실패
    if visited[target_r][target_c] == 0:
        return False

    # 공격 성공
    # 레이저 경로 체력 깎아주기
    global related
    directions = directions_2D[target_r][target_c]
    directions.pop(-1)  # 공격 대상은 경로 데미지에서 빼줘야
    cr, cc = attacker_r, attacker_c
    for direction in directions:
        cr, cc = move(cr, cc, direction)
        board[cr][cc] = max(board[cr][cc] - (board[attacker_r][attacker_c] // 2), 0)
        related.append([cr, cc])  # 공격 관련자 추가해주기


    # 공격 대상 체력 깎아주기
    board[target_r][target_c] = max(board[target_r][target_c] - board[attacker_r][attacker_c], 0)

    # 공격 관련자 추가해주기 : 공격 대상자
    related.append([attacker_r, attacker_c])
    related.append([target_r, target_c])

    return True

def bomb_attack(attacker_r, attacker_c, target_r, target_c):
    global related
    for d in range(8):
        nr, nc = move(target_r, target_c, d)
        if board[nr][nc] == 0 or (attacker_r == nr and attacker_c == nc):  # 이미 부셔진 포탑이나 자기 자신은 공격받지 않음
            continue
        board[nr][nc] = max(board[nr][nc] - (board[attacker_r][attacker_c] // 2), 0)
        related.append([nr, nc])  # 공격 관련자 추가해주기
    board[target_r][target_c] = max(board[target_r][target_c] - board[attacker_r][attacker_c], 0)

    # 공격 관련자 추가해주기
    related.append([target_r, target_c])
    related.append([attacker_r, attacker_c])


def check_tower_count():
    cnt = 0
    for i in range(N):
        for j in range(M):
            if board[i][j] != 0:
                cnt += 1
    return cnt


# 메인 턴
related = []  # 공격에 연관된 포탑 저장
for turn in range(1, K+1):
    related = []  # 매 턴마다 초기화

    attacker_r, attacker_c = select_attacker(turn)  # 공격자의 좌표
    target_r, target_c = select_target(attacker_r, attacker_c)  # 공격 대상자의 좌표

    is_laser_succeed = laser_attack(attacker_r, attacker_c, target_r, target_c)
    if not is_laser_succeed:
        bomb_attack(attacker_r, attacker_c, target_r, target_c)

    # 만약 부서지지 않은 포탑이 1개가 된다면 그 즉시 중지됩니다.
    tower_cnt = check_tower_count()
    if tower_cnt <= 1:
        break

    # for row in board:
    #     print(row)
    # print()

    # 포탑 정비
    for i in range(N):
        for j in range(M):
            if [i, j] not in related and board[i][j] != 0:
                board[i][j] += 1




# 마무리
max_attack_stat = -1  # 최대 공격력 찾기
for i in range(N):
    for j in range(M):
        if max_attack_stat < board[i][j]:
            max_attack_stat = board[i][j]

print(max_attack_stat)



"""
오늘의 배운점
방향의 우선순위를 가지고, 경로를 저장해야 하는 경우 

0. 우선순위에 맞게 dr. dc 배열을 만든다.
1. directions_2D 배열을 만든다
2. (cr, cc)에 저장된 경로에 새롭게 방문한 좌표를 넣는다 (visited[nr][nc] = visited[cr][cc] + 1 하는 느낌으로..) 

    visited = [[0 for _ in range(M)] for _ in range(N)]
    directions_2D = [[[] for _ in range(M)] for _ in range(N)]  # 이동방향을 저장한 2차원 배열

    # BFS 로직 시작
    q = deque()
    q.append([attacker_r, attacker_c])
    visited[attacker_r][attacker_c] = 1

    while q:
        cr, cc = q.popleft()
        for d in range(4):
            nr, nc = move(cr, cc, d)
            if visited[nr][nc] == 0 and board[nr][nc] != 0:
                visited[nr][nc] = visited[cr][cc] + 1
                directions_2D[nr][nc] = deepcopy(directions_2D[cr][cc])
                directions_2D[nr][nc].append(d)
                q.append([nr, nc])
"""
