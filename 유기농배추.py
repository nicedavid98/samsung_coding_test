from collections import deque

dx = [0,0,-1,1]
dy = [1,-1,0,0]

def BFS(start_x, start_y):
    global visited

    q = deque()
    q.append([start_x, start_y])
    visited[start_y][start_x] = 1

    while q:
        cx, cy = q.popleft()

        for d in range(4):
            nx = cx + dx[d]
            ny = cy + dy[d]
            # 경계를 벗어나지 않는다면
            if 0 <= nx <= M - 1 and 0 <= ny <= N - 1:
                # 다음 좌표가 배추이고, 방문하지 않았을 경우
                if board[ny][nx] == 1 and visited[ny][nx] == 0:
                    q.append([nx, ny])
                    visited[ny][nx] = 1


'''
<옮은 풀이> :  4-1-2 기억하기 

def BFS(start_x, start_y):
    global visited

    q = deque()
    q.append([start_x, start_y])
    visited[start_y][start_x] = 1  # 시작 노드를 큐에 넣으면서 바로 방문 처리

    while q:
        cx, cy = q.popleft()

        for d in range(4):
            nx = cx + dx[d]
            ny = cy + dy[d]
            # 경계를 벗어나지 않는다면
            if 0 <= nx <= M - 1 and 0 <= ny <= N - 1:
                # 다음 좌표가 배추이고, 방문하지 않았을 경우
                if board[ny][nx] == 1 and visited[ny][nx] == 0:
                    q.append([nx, ny])
                    visited[ny][nx] = 1  # 큐에 넣을 때 방문 처리

'''

'''
<틀린 풀이> : 중복된 좌표가 큐에 삽입되기 때문에 무한루프에 빠짐. 
def BFS(start_x, start_y):
    global visited

    q = deque()
    q.append([start_x, start_y])

    while q:
        cx, cy = q.popleft()
        visited[cy][cx] = 1  # 큐에서 꺼낼 때 방문 처리

        for d in range(4):
            nx = cx + dx[d]
            ny = cy + dy[d]
            # 경계를 벗어나지 않는다면
            if 0 <= nx <= M - 1 and 0 <= ny <= N - 1:
                # 다음 좌표가 배추이고, 방문하지 않았을 경우
                if board[ny][nx] == 1 and visited[ny][nx] == 0:
                    q.append([nx, ny])

'''


T = int(input())

# 테스트 케이스 반복
for _ in range(T):

    # 변수들 한번에 할당받는 방법 숙지하기
    M, N, K = map(int, input().split())

    count = 0  # 필요한 지렁이 개수
    visited = [[0 for _ in range(M)] for _ in range(N)]  # 방문 배열
    board = [[0 for _ in range(M)] for _ in range(N)]  # 배추밭 배열

    # 입력받은 배추밭 배추 심기
    for _ in range(K):
        x, y = map(int, input().split())
        board[y][x] = 1

    for x in range(M):
        for y in range(N):
            # 배추가 심어져 있고, 방문되지 않았을 경우 BFS 함수 호출하기
            if board[y][x] == 1 and visited[y][x] == 0:
                count += 1
                BFS(x, y)

    print(count)





