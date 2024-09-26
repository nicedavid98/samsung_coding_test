

# 전역변수 선언부
board = [[0 for _ in range(50)] for _ in range(50)]

santa_r = [None for _ in range(31)]
santa_c = [None for _ in range(31)]
santa_score = [None for _ in range(31)]
santa_stun = [-1 for _ in range(31)]
santa_fail = [None for _ in range(31)]
santa_exist = [None for _ in range(31)]
santa_strength = -1

rudolf_r = -1
rudolf_c = -1
rudolf_strength = -1


# 입력부 :
# 좌표는 (0,0) 부터 시작하는 것으로 보정, 산타 idx 는 1~30를 사용
N, M, P, rudolf_strength, santa_strength = map(int, input().split())
rudolf_r, rudolf_c = map(int, input().split())
rudolf_r -= 1
rudolf_c -= 1
board[rudolf_r][rudolf_c] = -1  # 루돌프는 맵에서 -1로 표기

for _ in range(P):
    idx, r, c = map(int, input().split())
    santa_r[idx] = r - 1
    santa_c[idx] = c - 1
    santa_score[idx] = 0
    santa_stun[idx] = -1
    santa_fail[idx] = False
    santa_exist[idx] = True
    board[santa_r][santa_c] = idx


def distance(r1, c1, r2, c2):
    return (r1 - r2)**2 + (c1 - c2)**2




def rudolf_move(turn):
    global rudolf_r, rudolf_c
    temp = []
    for idx in range(1, 31):
        if santa_exist[idx] and (not santa_fail[idx]):
            dist = distance(rudolf_r, rudolf_c, santa_r[idx], santa_c[idx])
            temp.append([dist, -1 * santa_r[idx], -1 * santa_c[idx], idx])
    temp.sort()
    target_santa_idx = temp[0][3]

    # 이쪽 산타로 움직일 예정
    target_santa_r, target_santa_c = santa_r[target_santa_idx], santa_c[target_santa_idx]

    # 루돌프 좌표 변경
    ddr = 0  # 움직일 방향 저장
    ddc = 0
    if target_santa_r == rudolf_r:
        if target_santa_c > rudolf_c:
            ddr += 0
            ddc += 1
        if target_santa_c < rudolf_c:
            ddr += 0
            ddc += -1
    elif target_santa_r > rudolf_r:
        if target_santa_c == rudolf_c:
            ddr += 1
            ddc += 0
        elif target_santa_c < rudolf_c:
            ddr += 1
            ddc += -1
        else:
            ddr += 1
            ddc += 1
    else:
        if target_santa_c == rudolf_c:
            ddr += -1
            ddc += 0
        elif target_santa_c < rudolf_c:
            ddr += -1
            ddc += -1
        else:
            ddr += -1
            ddc += 1

    # 루돌프 전역변수 업데이트
    prev_rudolf_r = rudolf_r
    prev_rudolf_c = rudolf_c
    rudolf_r += ddr
    rudolf_c += ddc

    #
    # 루돌프 이동 끝! 충돌 시작 (루돌프 맵 업데이트 X, 전역변수 업데이트 O)
    #

    # 루돌프가 빈공간으로 이동 : 맵만 업데이트하고 끝
    if board[rudolf_r][rudolf_c] == 0:
        board[prev_rudolf_r][prev_rudolf_c] = 0
        board[rudolf_r][rudolf_c] = -1
    # 루돌프가 산타가 있는 곳으로 이동
    elif board[rudolf_r][rudolf_c] >= 1:
        santa_idx = board[rudolf_r][rudolf_c]  # 그 자리에 있던 산타 인덱스

        santa_score[santa_idx] += rudolf_strength  # 산타가 점수 얻음

        next_santa_r = santa_r[santa_idx] + (ddr * rudolf_strength)
        next_santa_c = santa_c[santa_idx] + (ddc * rudolf_strength)

        # 연쇄작용 : 산타의 맵 좌표 업데이트, 산타 정보 업데이트 예정
        if not (0 <= next_santa_r <= N-1 and 0 <= next_santa_c <= N-1):  # 격자 밖이면
            board[santa_r[santa_idx]][santa_c[santa_idx]] = 0
            santa_fail[santa_idx] = True
        else:
            board[santa_r[santa_idx]][santa_c[santa_idx]] = 0

            while True:
                nnr = next_santa_r + ddr
                nnc = next_santa_r + ddc
                if board[nnr][nnc] == 0:
                    break





        # 루돌프 맵 업데이트
        board[prev_rudolf_r][prev_rudolf_c] = 0
        board[rudolf_r][rudolf_c] = -1

        # 기절
        santa_stun[santa_idx] = turn + 2


def santa_move(turn):
    dr = [-1,0,1,0]  # 상우하좌
    dc = [0,1,0,-1]
    for curr_santa_idx in range(1, 31):
        if not (santa_exist[curr_santa_idx] and (not santa_fail[curr_santa_idx]) and (turn >= santa_stun[curr_santa_idx])):
            continue
        curr_santa_r = santa_r[curr_santa_idx]
        curr_santa_c = santa_c[curr_santa_idx]

        cand = []
        if curr_santa_r > rudolf_r:
            cand.append(0)
        elif curr_santa_r < rudolf_r:
            cand.append(2)

        if curr_santa_c > rudolf_c:
            cand.append(3)
        elif curr_santa_c < rudolf_c:
            cand.append(1)

        cand.sort()

        # 해당 산타가 움직일 좌표 정하기
        next_dir = -1
        for d in cand:
            temp_next_santa_r = curr_santa_r + dr[d]
            temp_next_santa_c = curr_santa_c + dc[d]
            if board[temp_next_santa_r][temp_next_santa_c] == 0 or board[temp_next_santa_r][temp_next_santa_c] == -1:  # 움직일 칸이 비었거나, 루돌프라면
                if 0 <= temp_next_santa_r <= N-1 and 0 <= temp_next_santa_c <= N-1:  # 격자를 벗어나지 않으면
                    next_santa_r = temp_next_santa_r
                    next_santa_c = temp_next_santa_c
                    next_dir = d
                    break

        # 산타가 이동할 좌표
        next_santa_r = curr_santa_r + dr[next_dir]
        next_santa_c = curr_santa_c + dc[next_dir]

        # 산타 점수 획득
        santa_score[curr_santa_idx] += santa_strength

        # chain에서 산타의 맵 좌표 업데이트, 산타 정보 업데이트 예정
        over1 = chain(curr_santa_idx, next_santa_r, next_santa_c, dr[next_dir], dc[next_dir])
        if over1:
            return

        # 기절
        santa_stun[curr_santa_idx] = turn + 2



def solution():
    for t in range(M):

        rudolf_move(t)
        santa_move(t)

        # 탈락하지 않은 산타들에게 +1점
        for idx in range(1, 31):
            if santa_exist[idx] and (not santa_fail[idx]):
                santa_score[idx] += 1






