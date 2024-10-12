from copy import deepcopy
from collections import deque

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

board = []
knights = []
insts = []


# 입력부
L, N, Q = map(int, input().split())

for _ in range(L):
    row = list(map(int, input().split()))
    board.append(row)

for _ in range(N):
    knight = list(map(int, input().split()))
    knight[0] -= 1
    knight[1] -= 1
    knights.append(knight)

for _ in range(Q):
    inst = list(map(int, input().split()))
    inst[0] -= 1
    insts.append(inst)

first_knights = deepcopy(knights)  # 초기 상태의 기사들을 저장 (점수 계산을 위함)


def is_movable(knight_idx, dir):
    curr_r, curr_c, curr_h, curr_w, curr_k = knights[knight_idx]

    pos_list = []  # 해당 기사가 움직였을 때, 차지하게 될 좌표들의 리스트 [(r,c), ...]
    for i in range(curr_r + dr[dir], curr_r + dr[dir] + curr_h):
        for j in range(curr_c + dc[dir], curr_c + dc[dir] + curr_w):
            pos_list.append([i, j])

    # 벽이나 격자 밖이면 나가리
    for nr, nc in pos_list:
        if not (0 <= nr <= L-1 and 0 <= nc <= L-1):
            return False
        if board[nr][nc] == 2:
            return False
    return True


def find_next_knight(knight_idx, dir):
    next_knights_list = []  # 현재 knight_idx가 움직이면, 부딪히게 될 기사들의 인덱스 저장

    curr_r, curr_c, curr_h, curr_w, curr_k = knights[knight_idx]

    pos_list = []  # 해당 기사가 움직였을 때, 차지하게 될 좌표들의 리스트 [(r,c), ...]
    for i in range(curr_r + dr[dir], curr_r + dr[dir] + curr_h):
        for j in range(curr_c + dc[dir], curr_c + dc[dir] + curr_w):
            pos_list.append([i, j])

    # 모든 기사들을 순회
    for cand_idx in range(len(knights)):
        if cand_idx == knight_idx:  # 자기 자신은 제외
            continue
        if knights[cand_idx][4] <= 0:  # 살아 있어야..
            continue

        cand_r, cand_c, cand_h, cand_w, cand_k = knights[cand_idx]

        cand_pos_list = []  # 해당 기사가 차지하는 좌표들의 리스트 [(r,c), ...]
        for i in range(cand_r, cand_r + cand_h):
            for j in range(cand_c, cand_c + cand_w):
                cand_pos_list.append([i, j])

        for pos in pos_list:
            if pos in cand_pos_list:
                next_knights_list.append(cand_idx)
                break

    return next_knights_list


def cnt_trap(knight_idx, dir):
    curr_r, curr_c, curr_h, curr_w, curr_k = knights[knight_idx]

    cnt = 0
    for i in range(curr_r + dr[dir], curr_r + dr[dir] + curr_h):
        for j in range(curr_c + dc[dir], curr_c + dc[dir] + curr_w):
            if board[i][j] == 1:
                cnt += 1
    return cnt


# 메인 turn 시작 !!
for turn in range(Q):
    start_knight, turn_dir = insts[turn]

    # 명령을 받은 기사가 죽어있음
    if knights[start_knight][4] <= 0:
        continue

    # 움직일 수 있다면, 이를 처리해 주기 위해, 움직일 대상이 되는 기사 인덱스를 모두 표기
    moved_knights = []

    # queue를 생성하고, 명령을 받는 기사를 enqueue
    q = deque()
    q.append(start_knight)

    # queue가 빌 때 까지 반복
    can_move = True
    while q:
        curr_knight = q.popleft()

        # 죽었나요?
        if knights[curr_knight][4] <= 0:
            continue

        # 움직일 수 있나요? (벽, 격자 밖)
        if not is_movable(curr_knight, turn_dir):
            can_move = False
            break

        moved_knights.append(curr_knight)

        # 부딪히게 될 기사들의 목록을 큐에 추가
        next_knights = find_next_knight(curr_knight, turn_dir)  # 부딪히게 될 기사들의 목록
        for next_knight in next_knights:
            q.append(next_knight)

    # 움직일 수 있는 것으로 판정되었을 경우 : 실제로 리스트에서 움직이기
    if can_move:
        for moved_knight in moved_knights:
            if moved_knight != start_knight:
                num_trap = cnt_trap(moved_knight, turn_dir)
                knights[moved_knight][4] -= num_trap  # 여기서 체력 깎아줌
            knights[moved_knight][0] += dr[turn_dir]
            knights[moved_knight][1] += dc[turn_dir]


score = 0
for k in range(len(knights)):
    if knights[k][4] > 0:
        score += (first_knights[k][4] - knights[k][4])

print(score)


