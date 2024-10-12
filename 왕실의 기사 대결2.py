from copy import deepcopy
from collections import deque

dr = [-1,0,1,0]  # 상우하좌
dc = [0,1,0,-1]


# 전역변수
board = []
knight = []  # (r,c,h,w,체력), 유효 인덱스는 (1~N)
instructions = []  # (kidx, d)
first_knight = []  # 초기 상태의 기사

# 입력
L, N, Q = map(int, input().split())

for _ in range(L):
    temp = list(map(int, input().split()))
    board.append(temp)

knight = [[-1,-1,-1,-1,-1]]
for _ in range(N):
    r,c,h,w,k = map(int, input().split())
    knight.append([r-1, c-1, h, w, k])

first_knight = deepcopy(knight)

for _ in range(Q):
    i, d = map(int, input().split())
    instructions.append([i, d])



# kidx 기사가 차지하는 좌표를 리스트로 반환하는 함수
def knight_pos(kidx):
    pos_list = []
    curr_r, curr_c, height, width, health = knight[kidx]
    for i in range(curr_r, curr_r + height):
        for j in range(curr_c, curr_c + width):
            pos_list.append([i, j])
    return pos_list


# kidx 기사가 dir 방향으로 이동가능한지 판별. (벽인지, 격자 밖인지 )
def is_movable(kidx, dir):
    # 이동 후 기사가 위치할 좌표들의 리스트
    pos_list = []
    curr_r, curr_c, height, width, health = knight[kidx]
    next_r = curr_r + dr[dir]
    next_c = curr_c + dc[dir]
    for i in range(next_r, next_r + height):
        for j in range(next_c, next_c + width):
            pos_list.append([i, j])

    for r, c in pos_list:
        if not (0<=r<=L-1 and 0<=c<=L-1):  # 격자 밖인 것을 하나라도 발견
            return False
        if board[r][c] == 2:
            return False
    return True


# kidx 기사가 dir 방향으로 이동하였을때, 겹치는 기사의 리스트 반환 (움직임 처리하고 호출해도 무방)
def get_crash_knight_indice(kidx, dir):
    # 이동 후 기사가 위치할 좌표들의 리스트
    pos_list = []
    curr_r, curr_c, height, width, health = knight[kidx]
    next_r = curr_r + dr[dir]
    next_c = curr_c + dc[dir]
    for i in range(next_r, next_r + height):
        for j in range(next_c, next_c + width):
            pos_list.append([i, j])

    # 부딪히게 될 기사 인덱스 모음
    crash_knight_indice = []
    for r, c in pos_list:
        for nkidx in range(1, N+1):  # 모든 기사들을 순회
            if nkidx == kidx or knight[nkidx][4] <= 0:  # 자기 자신은 포함하지 말아야 + 죽은 기사는 무시해야
                continue
            next_knight_pos = knight_pos(nkidx)
            if [r, c] in next_knight_pos:
                crash_knight_indice.append(nkidx)

    # 중복 제거 후 리턴
    return list(set(crash_knight_indice))


# kidx 기사 좌표들에 속한 함정 숫자 반환
def count_trap(kidx):
    cnt = 0
    curr_r, curr_c, height, width, health = knight[kidx]
    for i in range(curr_r, curr_r + height):
        for j in range(curr_c, curr_c + width):
            if board[i][j] == 1:
                cnt += 1
    return cnt


def print_board():
    kboard = [[0 for _ in range(L)] for _ in range(L)]
    for i in range(1, N + 1):
        if knight[i][4] > 0:
            poses = knight_pos(i)
            for r, c in poses:
                kboard[r][c] = i
    for row in kboard:
        print(row)
    print()


def one_turn(start_idx, inst_dir):
    """
    1. 기사 이동
    """
    # 죽은 기사는 명령을 무시
    if knight[start_idx][4] <= 0:
        return

    # 시작 !
    can_move = True  # 움직일 수 있나요?
    moved_knight_indice = []  # 움직일 수 있을 경우 좌표 이동시켜줄 기사 인덱스들을 저장

    q = deque()
    q.append(start_idx)
    while q:
        curr_idx = q.popleft()
        moved_knight_indice.append(curr_idx)

        if not is_movable(curr_idx, inst_dir):  # 움직일 곳에 벽이거나 격자 밖이면
            can_move = False
            break

        crash_knight_indice = get_crash_knight_indice(curr_idx, inst_dir)  # 움직이면 부딪힐 친구들을 q에 삽입
        for idx in crash_knight_indice:
            q.append(idx)

    # 움직일 수 있으면 : 실제 이동 처리
    if can_move:
        for kidx in list(set(moved_knight_indice)):
            knight[kidx][0] += dr[inst_dir]
            knight[kidx][1] += dc[inst_dir]

    """
    2. 대결 데미지 
    """
    # 움직였어야 데미지 줌
    if can_move:
        # 데미지 처리해줄 기사들 리스트
        damage_knight_indice = deepcopy(moved_knight_indice)
        damage_knight_indice.remove(start_idx)  # 자기 자신은 데미지 안입음

        # 데미지 처리해줄 기사들 리스트 순회
        for didx in damage_knight_indice:
            trap_cnt = count_trap(didx)
            knight[didx][4] -= trap_cnt  # 체력 깎아줌

print_board()
# 메인 루프
for inst_idx in range(Q):

    idx, d = instructions[inst_idx]
    one_turn(idx, d)
    print_board()

answer = 0
for i in range(1, N+1):
    curr_r, curr_c, height, width, health = knight[i]
    if health > 0:
        answer += first_knight[i][4] - health

print(answer)



"""
느낀점:
1. 15일 전이랑 테케가 바뀌었다. 기존에 맞았던 것이 틀리게 됨
moved_knight_indice라는 리스트가 움직임의 대상이 되는 기사들을 모아놓은 리스트이다. 그리고 이 리스트를 큐, while문을 쓰며 채웠는데, 
연쇄작용을 하면서 중복으로 들어가는 기사가 존재할 수 있다는 점을 간과하고 있었다.

[0, 0, 3, 4, 0, 0, 0]
[1, 2, 3, 4, 6, 0, 0]
[1, 5, 5, 5, 6, 0, 0]
[0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0]

여기서 1번 기사를 오른쪽으로 민다고 생각해보자.. 그럼 6번 기사가 두번이나 리스트에 들어갈 것이다... 
=> 다른 그림으로도 생각해보자 (더 복잡하게)

2. 요즘 기본적인 핼퍼 함수들을 미리 구현해놓고 들어가는 걸 즐기는데, 이번에는 좀 도가 지나쳤던 것 같다.
미리 함수를 만드려니까 나중에 추가해야 할 로직도 생기고 좋지 않은듯 . 적당히 하자  
"""

