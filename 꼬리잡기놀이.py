from collections import deque


dr = [0,-1,0,1]  # 우상좌하
dc = [1,0,-1,0]

# 전역변수
board = []
N, M, K = -1, -1, -1
answer = 0

# 입력부
N, M, K = map(int, input().split())

for _ in range(N):
    temp = list(map(int, input().split()))
    board.append(temp)

def print_board():
    for row in board:
        print(row)
    print()


def in_range(r, c):
    if 0<=r<=N-1 and 0<=c<=N-1:
        return True
    return False

# head 좌표를 입력해야 작동 : 머리부터 1,2,3,4,5... 순으로 visited 배열을 반환
def head_BFS(start_r, start_c):

    visited = [[0 for _ in range(N)] for _ in range(N)]
    q = deque()

    q.append([start_r, start_c])
    visited[start_r][start_c] = 1
    while q:
        cr, cc = q.popleft()
        for dir in range(4):
            nr = cr + dr[dir]
            nc = cc + dc[dir]
            if in_range(nr, nc) and visited[nr][nc] == False and board[nr][nc] != 0:  # 이동 선안이고, 격자 안이고, 방문하지 않았을 때
                if board[cr][cc] == board[nr][nc] or board[cr][cc] + 1 == board[nr][nc]:  # 다음 칸이 숫자가 같거나, 1 클때
                    q.append([nr, nc])
                    visited[nr][nc] = visited[cr][cc] + 1

    return visited

# 일반 좌표를 입력해도 작동 : 해당 그룹의 좌표는 다 1로 표시한 visited 배열을 반환
def BFS(start_r, start_c):

    visited = [[0 for _ in range(N)] for _ in range(N)]
    q = deque()

    q.append([start_r, start_c])
    visited[start_r][start_c] = 1
    while q:
        cr, cc = q.popleft()
        for dir in range(4):
            nr = cr + dr[dir]
            nc = cc + dc[dir]
            if in_range(nr, nc) and visited[nr][nc] == False and board[nr][nc] != 0:  # 이동 선안이고, 격자 안이고, 방문하지 않았을 때
                q.append([nr, nc])
                visited[nr][nc] = 1

    return visited


def move():

    head_pos_list = []  # 머리사람들의 좌표를 담은 리스트
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:  # 머리사람 찾음
                head_pos_list.append([i, j])

    # 모든 머리사람들을 기준으로 그룹들을 순회
    for head_r, head_c in head_pos_list:
        visited = head_BFS(head_r, head_c)

        middle_pos = []  # 중간 좌표들 모음
        tail_r, tail_c = -1, -1  # 꼬리사람 좌표
        road_pos = []  # 이동 선들의 좌표
        for r in range(N):
            for c in range(N):
                if visited[r][c] != 0:
                    if board[r][c] == 2:
                        middle_pos.append([r, c])
                    elif board[r][c] == 3:
                        tail_r, tail_c = r, c
                    elif board[r][c] == 4:
                        road_pos.append([r, c])


        # 이동 선 움직이기
        for road_r, road_c in road_pos:
            for d in range(4):
                road_nr = road_r + dr[d]
                road_nc = road_c + dc[d]
                if in_range(road_nr, road_nc) and board[road_nr][road_nc] == 3:
                    board[road_nr][road_nc] = 4

        # 꼬리사람 움직이기
        for d in range(4):
            tail_nr = tail_r + dr[d]
            tail_nc = tail_c + dc[d]
            if in_range(tail_nr, tail_nc) and board[tail_nr][tail_nc] == 2:
                board[tail_nr][tail_nc] = 3

        # 중간 사람들 춤직이기
        for mid_r, mid_c in middle_pos:
            for d in range(4):
                mid_nr = mid_r + dr[d]
                mid_nc = mid_c + dc[d]
                if in_range(mid_nr, mid_nc) and board[mid_nr][mid_nc] == 1:
                    board[mid_nr][mid_nc] = 2

        # 머리사람 움직이기
        is_three = False
        for d in range(4):
            head_nr = head_r + dr[d]
            head_nc = head_c + dc[d]
            if in_range(head_nr, head_nc) and board[head_nr][head_nc] == 4:
                board[head_nr][head_nc] = 1
                is_three = True
                break

        if not is_three:
            # 4가 없으면, 머리사람은 3을 따라가야.
            for d in range(4):
                head_nr = head_r + dr[d]
                head_nc = head_c + dc[d]
                if in_range(head_nr, head_nc) and board[head_nr][head_nc] == 3:
                    board[head_nr][head_nc] = 1
    # print()


# 인자 turn은 0부터 시작하는 것으로 정한다
def throw_ball(turn):
    throw_list = []  # turn을 인덱스로 하며 공을 던지는 [r,c,dir] 저장
    for i in range(N):
        throw_list.append([i, 0, 0])
    for i in range(N):
        throw_list.append([N-1, i, 1])
    for i in range(N):
        throw_list.append([N-1-i, N-1, 2])
    for i in range(N):
        throw_list.append([0, N-1-i, 3])

    # 현재 공을 던지는 정보
    hit_r, hit_c = -1, -1  # 공을 맞는 사람의 좌표

    curr_r, curr_c, curr_dir = throw_list[turn]
    for jump in range(N):  # 7칸이면 (0-6)
        next_r = curr_r + (dr[curr_dir] * jump)
        next_c = curr_c + (dc[curr_dir] * jump)
        if in_range(next_r, next_c) and 1 <= board[next_r][next_c] <= 3:
            hit_r = next_r
            hit_c = next_c
            break  # break 해줘야 최초로 맞은 사람만 체크하고 떠남

    # 1. 공에 맞은 사람이 아무도 없는 경우
    if hit_r == -1 and hit_c == -1:
        return

    # 2. 공에 맞은 사람이 있는 경우
    # 공에 맞은 그룹의 헤드 좌표 구하기
    head_r, head_c = -1, -1
    visited_for_finding_head = BFS(hit_r, hit_c)
    for i in range(N):
        for j in range(N):
            if visited_for_finding_head[i][j] != 0 and board[i][j] == 1:
                head_r, head_c = i, j

    # head로 부터 몇번째 사람인지 구하기
    visited = head_BFS(head_r, head_c)
    head_num = visited[head_r][head_c]
    hit_num = visited[hit_r][hit_c]

    # 점수 내기
    global answer
    answer += (hit_num - head_num + 1) ** 2

    # head와 tail 바꾸기
    tail_r, tail_c = -1, -1  # 꼬리사람 좌표
    for r in range(N):
        for c in range(N):
            if visited[r][c] != 0 and board[r][c] == 3:
                tail_r, tail_c = r, c
                break
    board[tail_r][tail_c] = 1
    board[head_r][head_c] = 3
    # print()



# 메인 루프
for round in range(K):
    move()
    # print_board()
    turn = round % (4*N)
    throw_ball(turn)

print(answer)


"""
느낀점:

1. 마찬가지로.. 순회할때, 이미 움직인 친구들이 중복 적용되지 않도록 조심..

이렇게 고쳤음
head_pos_list = []  # 머리사람들의 좌표를 담은 리스트
    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:  # 머리사람 찾음
                head_pos_list.append([i, j])

    # 모든 머리사람들을 기준으로 그룹들을 순회
    for head_r, head_c in head_pos_list:
        # 여기서 움직임이 있음 
        
2. 문제를 잘읽자 : 공쏘는 모양을 대충 봤다가 틀림 
"""


