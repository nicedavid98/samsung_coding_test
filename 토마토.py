from collections import deque

dr = [0,0,-1,1]
dc = [1,-1,0,0]

def BFS():
    global visited, q
    while q:
        cr, cc = q.popleft()
        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]
            if 0 <= nr <= N-1 and 0 <= nc <= M-1:
                if visited[nr][nc] == 0 and board[nr][nc] == 0:
                    q.append([nr, nc])
                    visited[nr][nc] = visited[cr][cc] + 1


M, N = map(int, input().split())

# 격자 형태로 주어진 배열 입력받는 방법 숙지
board = []
for _ in range(N):
    row = list(map(int, input().split()))
    board.append(row)

# queue와 visited 베열 생성
q = deque()
visited = [[0 for _ in range(M)] for _ in range(N)]

# 여러 시작점이 존재하기 때문에, 미리 queue 삽입하기.
for i in range(N):
    for j in range(M):
        if board[i][j] == 1:
            q.append([i, j])
            visited[i][j] = 1  # 혼동 방지를 위해 1일차부터 시작

# BFS 함수 실행 => visited 베열에 발자취 저장
BFS()

# visited 배열을 확인하며 답을 찾기
answer = -1
for i in range(N):
    for j in range(M):
        if board[i][j] != -1 and visited[i][j] > answer:
            answer = visited[i][j] - 1

# 토마토가 모두 익지 못한 상황 check
for i in range(N):
    for j in range(M):
        if board[i][j] == 0 and visited[i][j] == 0:
            answer = -1

print(answer)




