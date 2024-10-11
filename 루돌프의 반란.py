
dr = [-1,0,1,0]  # 북동남서
dc = [0,1,0,-1]

# 전역변수
N, M, P, C, D = -1,-1,-1,-1,-1
rudolf_r, rudolf_c = -1, -1
santa_list = []

# 입력부
N, M, P, C, D = map(int, input().split())

rudolf_r, rudolf_c = map(int, input().split())
rudolf_r -= 1  # 좌표 기준이 (1,1) 이므로 처리
rudolf_c -= 1

santa_list = [[-1, -1, -1, False, 0] for _ in range(P+1)]  # 산타 번호를 인덱스로 쓰면 됨. 유효한 인덱스 범위는 (1, P)
for _ in range(P):
    idx, r, c = map(int, input().split())
    santa_list[idx] = [r-1, c-1, -1, True, 0]


def calculate_dist(r1, c1, r2, c2):
    return (r1-r2)**2 + (c1-c2)**2


def is_inside(r, c):
    if 0<=r<=N-1 and 0<=c<=N-1:
        return True
    return False


# 해당 좌표에 산타가 있으면 True (산타 배열을 순회함)
def is_there_santa(r, c):
    for sidx in range(1, P+1):
        cr, cc, shock, alive, score = santa_list[sidx]
        if (cr == r and cc == c) and alive:  # 살아있는 산타만
            return True
    return False


# 해당 좌표에 살아있는 산타가 있으면 그 산타의 인덱스 반환 (산타 배열을 순회함)
def find_santa_idx_by_pos(r, c):
    for sidx in range(1, P+1):
        cr, cc, shock, alive, score = santa_list[sidx]
        if (cr == r and cc == c) and alive:  # 살아있는 산타만
            return sidx
    return -1


# 루돌프 이동 후 좌표를 전역변수에 반영해줌
def rudolf_move(turn):
    global rudolf_r, rudolf_c

    #  가장 가까운 산타를 찾아보자
    santa_cand = []  # (dist, r, c, sidx)
    for sidx in range(1, P+1):
        cr, cc, shock, alive, score = santa_list[sidx]
        if alive:  # 탈락하지 않은 산타 중
            santa_cand.append([calculate_dist(rudolf_r, rudolf_c, cr, cc), -cr, -cc, sidx])
    santa_cand.sort()

    # 산타 선택 완료
    selected_santa_idx = santa_cand[0][3]  # 선택된 산타 인덱스
    sr, sc = santa_list[selected_santa_idx][0], santa_list[selected_santa_idx][1]  # 선택된 산타의 좌표

    # 루돌프 이동 정하기
    dir_r, dir_c = 0, 0
    if rudolf_r > sr:
        dir_r = -1
    elif rudolf_r < sr:
        dir_r = 1

    if rudolf_c > sc:
        dir_c = -1
    elif rudolf_c < sc:
        dir_c = 1

    # 루돌프 이동 처리
    rudolf_r += dir_r
    rudolf_c += dir_c

    # 충돌 !
    if rudolf_r == sr and rudolf_c == sc:
        rudolf_crash(turn, selected_santa_idx, dir_r, dir_c)


def santa_move(turn):
    for sidx in range(1, P+1):
        if santa_list[sidx][3] and santa_list[sidx][2] < turn:  # 탈락하지 않았거나, 기절상태가 아닌 산타만

            curr_r, curr_c, shock, alive, score = santa_list[sidx]  # 현재 보고있는 산타

            # 최단거리 찾기
            min_dist = 100000000
            for dir in range(4):
                nr = curr_r + dr[dir]
                nc = curr_c + dc[dir]
                if is_inside(nr, nc) and not is_there_santa(nr, nc) and calculate_dist(rudolf_r, rudolf_c, curr_r, curr_c) > calculate_dist(rudolf_r, rudolf_c, nr, nc):  # 거리가 더 가까워져야함 + 격자 안이고, 그곳에 산타가 없을 때
                    if min_dist > calculate_dist(rudolf_r, rudolf_c, nr, nc):
                        min_dist = calculate_dist(rudolf_r, rudolf_c, nr, nc)

            # 움직일 방향 찾기
            next_dir = -1
            for dir in range(4):
                nr = curr_r + dr[dir]
                nc = curr_c + dc[dir]
                if is_inside(nr, nc) and not is_there_santa(nr, nc) and calculate_dist(rudolf_r, rudolf_c, curr_r, curr_c) > calculate_dist(rudolf_r, rudolf_c, nr, nc):  # 거리가 더 가까워져야함 + 격자 안이고, 그곳에 산타가 없을 때
                    if min_dist == calculate_dist(rudolf_r, rudolf_c, nr, nc):
                        next_dir = dir
                        break  # 끊어줘야지 ㅆㅂ

            # 움직였을 때
            if next_dir != -1:
                # 산타 이동 처리
                santa_list[sidx][0] = curr_r + dr[next_dir]
                santa_list[sidx][1] = curr_c + dc[next_dir]

                # 충돌 !
                if rudolf_r == santa_list[sidx][0] and rudolf_c == santa_list[sidx][1]:
                    santa_crash(turn, sidx, dr[next_dir], dc[next_dir])


# crash 함수가 그 턴에 움직인 루돌프와 산타의 좌표는 이미 변경되었음에 유의
# 루돌프가 박음
def rudolf_crash(turn, santa_idx, dir_r, dir_c):

    # 피해 산타가 밀려난 좌표
    next_r = santa_list[santa_idx][0] + (dir_r * C)
    next_c = santa_list[santa_idx][1] + (dir_c * C)

    # 피해 산타의 점수는 지금 처리해주자 (밀려난 좌표는 연쇄작용 후 처리)
    santa_list[santa_idx][4] += C
    # 피해 산타의 기절 처리
    santa_list[santa_idx][2] = turn + 1

    # 격자 밖으로 밀려나 탈락한 경우
    if not is_inside(next_r, next_c):
        santa_list[santa_idx][3] = False
    # 밀려난 곳에 산타가 있는 경우 : 상호작용
    elif is_there_santa(next_r, next_c):
        chain(next_r, next_c, dir_r, dir_c)

    # 최종적으로, 밀려난 좌표 연쇄작용 후 처리
    santa_list[santa_idx][0] = next_r
    santa_list[santa_idx][1] = next_c


# crash 함수가 그 턴에 움직인 루돌프와 산타의 좌표는 이미 변경되었음에 유의
# 산타가 박음
def santa_crash(turn, santa_idx, dir_r, dir_c):

    # 산타가 반대로 밀려난 좌표
    next_r = santa_list[santa_idx][0] + ((-1 * dir_r) * D)
    next_c = santa_list[santa_idx][1] + ((-1 * dir_c) * D)

    # 산타의 점수는 지금 처리해주자 (밀려난 좌표는 연쇄작용 후 처리)
    santa_list[santa_idx][4] += D

    # 피해 산타의 기절 처리
    santa_list[santa_idx][2] = turn + 1

    # 격자 밖으로 밀려나 탈락한 경우
    if not is_inside(next_r, next_c):
        santa_list[santa_idx][3] = False
    # 밀려난 곳에 산타가 있는 경우 : 상호작용
    elif is_there_santa(next_r, next_c):
        chain(next_r, next_c, -1 * dir_r, -1 * dir_c)

    # 최종적으로, 밀려난 좌표 연쇄작용 후 처리
    santa_list[santa_idx][0] = next_r
    santa_list[santa_idx][1] = next_c


# start_r, start_c는 연쇄작용이 시작되는 좌표, 아직 가해자 산타 좌표 업데이트 안한 상태
def chain(start_r, start_c, dir_r, dir_c):
    # 이동 처리해줘야 할 산타 idx 목록 (날라온 가해 산타는 포함되서는 안됨)
    moved_santa_indices = []

    curr_r, curr_c = start_r, start_c  # 이 좌표에는 아직 가해자 산타가 반영되지 않았음에 주의
    while True:
        if not is_there_santa(curr_r, curr_c):
            break
        else:
            moved_santa_indices.append(find_santa_idx_by_pos(curr_r, curr_c))

        curr_r += dir_r
        curr_c += dir_c

    # 연쇄작용 후 좌표를 반영해볼까
    for sidx in moved_santa_indices:
        moved_santa_nr = santa_list[sidx][0] + dir_r
        moved_santa_nc = santa_list[sidx][1] + dir_c
        if is_inside(moved_santa_nr, moved_santa_nc):  # 격자 안이면
            # 산타 배열에 이동 반영
            santa_list[sidx][0] = moved_santa_nr
            santa_list[sidx][1] = moved_santa_nc
        else:  # 격자 밖이면 탈락
            santa_list[sidx][3] = False


def give_point():
    for sidx in range(1, P+1):
        cr, cc, shock, alive, score = santa_list[sidx]
        if alive:  # 살아있는 산타가 있으면
            santa_list[sidx][4] += 1


def is_game_over():
    for sidx in range(1, P+1):
        cr, cc, shock, alive, score = santa_list[sidx]
        if alive:  # 살아있는 산타가 있으면 바로 False 반환
            return False
    return True


def print_answer():
    for sidx in range(1, P+1):
        cr, cc, shock, alive, score = santa_list[sidx]
        print(score, end=" ")


def print_board(turn):
    board = [[0 for _ in range(N)] for _ in range(N)]
    for sidx in range(1, P+1):
        cr, cc, shock, alive, score = santa_list[sidx]
        if alive:
            board[cr][cc] = sidx
    board[rudolf_r][rudolf_c] = -1

    print("turn: ", turn+1)
    for row in board:
        print(row)
    print()


# 메인 루프
for turn in range(M):
    # print_board(turn)

    rudolf_move(turn)
    if is_game_over():
        break
    # print_board(turn)

    santa_move(turn)
    if is_game_over():
        break
    # print_board(turn)

    give_point()

print_answer()


"""
느낀점:
1. 방향 우선순위 => break 까먹지 말기
2. 거리 계산에 유의 ! 이번에는 제곱 형식이라 우리가 직관적으로 생각하는 거리가 아니었음. (문제 잘읽고 자의로 판단하지 말기)

# 최단거리 찾기
min_dist = 100000000
for dir in range(4):
    nr = curr_r + dr[dir]
    nc = curr_c + dc[dir]
    if is_inside(nr, nc) and not is_there_santa(nr, nc) and calculate_dist(rudolf_r, rudolf_c, curr_r, curr_c) > calculate_dist(rudolf_r, rudolf_c, nr, nc):  # 거리가 더 가까워져야함 + 격자 안이고, 그곳에 산타가 없을 때
        if min_dist > calculate_dist(rudolf_r, rudolf_c, nr, nc):
            min_dist = calculate_dist(rudolf_r, rudolf_c, nr, nc)

# 움직일 방향 찾기
next_dir = -1
for dir in range(4):
    nr = curr_r + dr[dir]
    nc = curr_c + dc[dir]
    if is_inside(nr, nc) and not is_there_santa(nr, nc) and calculate_dist(rudolf_r, rudolf_c, curr_r, curr_c) > calculate_dist(rudolf_r, rudolf_c, nr, nc):  # 거리가 더 가까워져야함 + 격자 안이고, 그곳에 산타가 없을 때
        if min_dist == calculate_dist(rudolf_r, rudolf_c, nr, nc):
            next_dir = dir
            break  # 끊어줘야지 ㅆㅂ
            

3. 이동을 언제 처리해줘야 할지 잘 설계해서 푼것같음 뿌듯 ㅋ
이동을 언제 처리할지에 대한 계획이 잡힌 상태에서 구현 들어가자 

4. 역시 함수를 나눠서 처리하는 게 좋음
그 전에 풀었을 때에는 루돌프 움직임 => 산타 튕기고 => 연쇄 와 같이 큰 단위로 함수를 만들어 풀어서 코드 중복이 많았고 디버깅이 진자 어려웠음 

"""

