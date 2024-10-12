from collections import deque

dr = [-1,0,0,1]
dc = [0,-1,1,0]

N, M = map(int, input().split())

board = []  # 베이스캠프와 편의점 위치를 기록한 맵, 베이스캡프는 1, 편의점은 2 => 이동 불가가 되면 각각 10을 더해줌
people_board =[[[] for _ in range(N)] for _ in range(N)]  # 실시간 사람들의 위치를 기록한 맵
store_by_people = [[-1, -1]]  # 사람들이 가고싶어 하는 편의점의 좌표를 기록하는 배열. 단 사람의 idx는 1부터 시작
complete_people = [False for _ in range(M + 1)]  # 사람이 편의점에 도착했는지 트래킹하는 배열


# 입력부
for _ in range(N):
    temp_row = list(map(int, input().split()))
    board.append(temp_row)

for _ in range(M):
    r, c = map(int, input().split())
    store_by_people.append([r - 1, c - 1])
    board[r-1][c-1] = 2


def is_inside(r, c):
    if 0<=r<=N-1 and 0<=c<=N-1:
        return True
    else:
        return False


# 다음에 이동할 방향을 리턴해주는 함수
def find_next_dir(start_r, start_c, target_r, target_c):
    visited = [[0 for _ in range(N)] for _ in range(N)]
    route_record = [[[] for _ in range(N)] for _ in range(N)]  # 이동한 방향을 저장하는 배열
    q = deque()

    visited[start_r][start_c] = 1
    q.append([start_r, start_c])
    while q:
        cr, cc = q.popleft()
        for dir in range(4):
            nr = cr + dr[dir]
            nc = cc + dc[dir]
            if is_inside(nr, nc) and board[nr][nc] < 10:  # 격자 안이거나, 움직일 수 있으면
                if not visited[nr][nc]:
                    q.append([nr, nc])
                    visited[nr][nc] = 1
                    route_record[nr][nc] = route_record[cr][cc] + [dir]  # 경로 기록
                    if nr == target_r and nc == target_c:
                        next_dir = route_record[nr][nc][0]
                        return next_dir  # 편의점을 만나면, 다음에 이동할 방향을 리턴해줌


# 이동할 베이스캠프를 정해 좌표를 리턴하는 함수
def find_base_camp(start_r, start_c):
    visited = [[0 for _ in range(N)] for _ in range(N)]
    q = deque()
    visited[start_r][start_c] = 1
    q.append([start_r, start_c])
    while q:
        cr, cc = q.popleft()
        for dir in range(4):
            nr = cr + dr[dir]
            nc = cc + dc[dir]
            if is_inside(nr, nc) and board[nr][nc] < 10:  # 격자 안이거나, 움직일 수 있으면
                if not visited[nr][nc]:
                    q.append([nr, nc])
                    visited[nr][nc] = visited[cr][cc] + 1

    # visited 기록 끝 : 이제 어디 베이스캠프 갈지 정해보자
    min_dist = 10000000
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1 and visited[i][j] != 0:  # 베이스캠프면서, 방문할 수 있어야
                if min_dist > visited[i][j]:
                    min_dist = visited[i][j]

    base_cand = []  # 최단거리인 베이스캠프 후보(좌표)들
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1 and visited[i][j] != 0:  # 베이스캠프면서, 방문할 수 있어야
                if min_dist == visited[i][j]:
                    base_cand.append([i, j])

    # 행=>렬 이 작은 놈으로 선택
    base_cand.sort()
    return base_cand[0]


def step1():
    inside_peoples = []  # [idx, r, c] 로 이루어진 배열. 현재 격자 위에 존재하는 사람들의 좌표를 기록
    for i in range(N):
        for j in range(N):
            if people_board[i][j]:
                for people in people_board[i][j]:
                    inside_peoples.append([people, i, j])

    # 격자 내의 모든 사람들 이동 !
    for people in inside_peoples:
        pidx, cr, cc = people
        target_r, target_c = store_by_people[pidx]  # 타켓 편의점 좌표

        next_direction = find_next_dir(cr, cc, target_r, target_c)  # 다음에 이동할 방향
        nr = cr + dr[next_direction]
        nc = cc + dc[next_direction]

        # 이동 처리
        people_board[nr][nc].append(pidx)
        people_board[cr][cc].remove(pidx)


def step2():
    inside_peoples = []  # [idx, r, c] 로 이루어진 배열. 현재 격자 위에 존재하는 사람들의 좌표를 기록
    for i in range(N):
        for j in range(N):
            if people_board[i][j]:
                for people in people_board[i][j]:
                    inside_peoples.append([people, i, j])

    # 격자 내의 모든 사람들 대상 순회
    for people in inside_peoples:
        pidx, cr, cc = people
        target_r, target_c = store_by_people[pidx]  # 타켓 편의점 좌표

        if cr == target_r and cc == target_c:  # 타겟 편의점에 도착했다면
            board[cr][cc] = 12  # 이동불가 좌표 처리
            people_board[cr][cc].remove(pidx)  # 목표 편의점에 도착했음으로 사람 맵에서 지워줌
            complete_people[pidx] = True  # 목표 완수 사람 배열에 표시


def step3(turn):
    if turn <= M:
        store_r, store_c = store_by_people[turn]
        base_r, base_c = find_base_camp(store_r, store_c)

        people_board[base_r][base_c].append(turn)  # 베이스캠프에 사람 배치
        board[base_r][base_c] = 11  # 이동 불가 좌표 기록


# 메인 루프
is_game_over = False
turn = 1  # turn 수는 1부터 시작
while not is_game_over:
    # 로직
    step1()
    step2()
    step3(turn)

    # 로직 종료 후
    cnt_complete_people = 0
    for i in range(1, M+1):
        if complete_people[i] == True:
            cnt_complete_people += 1
    if cnt_complete_people == M:
        is_game_over = True

    if is_game_over:
        break
    turn += 1

print(turn)


'''
느낀 점

1. 하나의 격자에 여러 사람이 존재할 수 있으면, 
=> 격자로 사람을 관리하는 것은 비추이다 
=> 사람에 대한 배열을 만든 뒤, 좌표를 저장하는 것이 나은 선택일 듯 

2. 못찾았던 실수 내용: find_base_camp
=> find_base_camp에서 '방문할 수 있는 베이스 캠프' 중에서 최단거리인 베이스캠프를 찾았어야 하는데, 그 조건을 빼먹음 
이렇게 해야 하는데 if board[i][j] == 1 and visited[i][j] != 0:
이렇게 실수함 if board[i][j] == 1:  # 베이스캠프면서, 방문할 수 있어야
'''
