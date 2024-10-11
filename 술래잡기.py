from copy import deepcopy

dr = [-1,0,1,0]  # 북우하좌
dc = [0,1,0,-1]

# 전역변수
N, M, H, K = -1,-1,-1,-1
board = []  # 나무는 1로 표시
tagger_r, tagger_c, tagger_dir = -1, -1, -1
runner = []  # 도망자들의 정보를 저장 [r, c, dir, is_alive]
answer = -1


# 입력부
N, M, H, K = map(int, input().split())
board = [[0 for _ in range(N)] for _ in range(N)]
tagger_r, tagger_c = N // 2, N // 2  # 술래 좌표
tagger_dir = -1
runner = []
answer = 0

for _ in range(M):
    x, y, d = map(int, input().split())
    runner.append([x-1, y-1, d, True])

for _ in range(H):
    x, y = map(int, input().split())
    board[x-1][y-1] = 1


# 술래의 이동방향을 리스트에 담아 리턴해주는 함수
def make_tagger_move_list():
    tagger = []
    tagger_move = []
    temp_dir = 0
    for cont in range(1, N): # (1 ~ N-1): 몇번 연속되는지
        for i in range(2):
            for j in range(cont):
                tagger_move.append(temp_dir)
            temp_dir = (temp_dir + 1) % 4
    for _ in range(N-1):
        tagger_move.append(temp_dir)

    tagger_move_opposite = deepcopy(tagger_move)
    tagger_move_opposite.reverse()
    for i in range(len(tagger_move_opposite)):
        if tagger_move_opposite[i] == 0:
            tagger_move_opposite[i] = 2
        elif tagger_move_opposite[i] == 1:
            tagger_move_opposite[i] = 3
        elif tagger_move_opposite[i] == 2:
            tagger_move_opposite[i] = 0
        elif tagger_move_opposite[i] == 3:
            tagger_move_opposite[i] = 1

    while len(tagger) <= K:
        tagger += tagger_move
        tagger += tagger_move_opposite

    return tagger[0:K+1]


def calculate_dist(r1, c1, r2, c2):
    return abs(r1-r2) + abs(c1-c2)


def is_inside(r, c):
    if 0<=r<=N-1 and 0<=c<=N-1:
        return True
    return False


def runner_move():
    # 모든 도망자를 순회
    for ridx in range(len(runner)):
        curr_r, curr_c, curr_dir, curr_alive = runner[ridx]
        if curr_alive == True and calculate_dist(tagger_r, tagger_c, curr_r, curr_c) <= 3:  # 살아있고, 술래와 거리가 3 이하인 도망자들만
            # 도망자가 움직일 좌표
            nr = curr_r + dr[curr_dir]
            nc = curr_c + dc[curr_dir]
            if not is_inside(nr, nc):  # 격자 밖이라면
                nr = curr_r + dr[(curr_dir + 2) % 4]
                nc = curr_c + dc[(curr_dir + 2) % 4]
                runner[ridx][2] = (curr_dir + 2) % 4  # 바뀐 방향도 적용해줘야

            # 이동한 곳에 술래가 없다면
            if not (tagger_r == nr and tagger_c == nc):
                runner[ridx][0], runner[ridx][1] = nr, nc  # 이동 확정 및 기록

# 아마 마지막 인덱스 참조 오류가 뜰것
# turn 은 0부터 시작
def tagger_move(turn):
    tagger_dir_list = make_tagger_move_list()  # 술래의 이동 방향이 적혀있는 배열

    turn_dir = tagger_dir_list[turn]  # 지금 당장 이동할 방향

    global tagger_r, tagger_c, tagger_dir  # 이동+방향 확정 및 기록 !
    tagger_r += dr[turn_dir]
    tagger_c += dc[turn_dir]
    tagger_dir = tagger_dir_list[turn + 1]  # 이동 후의 위치가 만약 이동방향이 틀어지는 지점이라면, 방향을 바로 틀어줍니다.

    # 도망자 잡기 시작 !!!
    for step in range(3):
        # 현재 보고있는 좌표를 나타냄
        eye_r = tagger_r + (dr[tagger_dir] * step)
        eye_c = tagger_c + (dc[tagger_dir] * step)

        if not is_inside(eye_r, eye_c):  # 해당 좌표가 격자 밖인 경우
            continue
        if board[eye_r][eye_c] == 1:  # 해당 좌표가 나무인 경우
            continue

        # 모든 도망자를 순회
        for ridx in range(len(runner)):
            curr_r, curr_c, curr_dir, curr_alive = runner[ridx]
            if curr_alive == True and (eye_r == curr_r and eye_c == curr_c):  # 살아있으면서 현재 시야에 잡힌 놈
                runner[ridx][3] = False  # 죽여
                global answer
                answer += (turn + 1)  # turn은 0부터 시작하므로 처리


# 메인 루프
for turn in range(K):
    runner_move()
    tagger_move(turn)

print(answer)


"""
느낀점 

1. 실수는 안했지만 마찬가지로, 한 좌표에 여러 사람이 들어갈 수 있으면 갹자로 관리하기보다는 그냥 배열로 관리하는 것이 편할지도 
2. 방향을 바꾸는 시점에 유의해서 반영해 주어야 
"""








