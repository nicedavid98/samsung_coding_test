
# 상(0) 하(1) 좌(2) 우(3)
dr = [-1,1,0,0]
dc = [0,0,-1,1]

N, M, K = map(int, input().split())

board = []  # 맵
travelers = [[-1,-1, True]]  # 참가자들의 좌표를 기록하는 배열. 인덱스 1부터 시작

for _ in range(N):
    temp_row = list(map(int, input().split()))
    board.append(temp_row)

for _ in range(M):
    temp_r, temp_c = map(int, input().split())
    travelers.append([temp_r-1, temp_c-1, False])  # [r좌표, c좌표, 탈출여부(탈출했으면 True)]

exit_r, exit_c = map(int, input().split())  # 출구 좌표
exit_r -= 1
exit_c -= 1
board[exit_r][exit_c] = 100  # 맵에서 출구는 100로 표시


def dist(r1, c1, r2, c2):
    return abs(r1-r2) + abs(c1-c2)


def move():
    # 움직인 횟수 저장
    move_cnt = 0

    # 모든 참가자를 순회
    for curr in travelers:
        curr_r, curr_c, is_exit = curr
        if curr_r == -1 and curr_c == -1:  # 인덱스 0번에 잇는 참여자는 허수라서 제외
            continue

        if curr[2] == True:  # 아직 탈출 못한 사람만 !
            continue

        dir_cand = []
        for d in range(4):
            if dist(curr_r, curr_c, exit_r, exit_c) > dist(curr_r + dr[d], curr_c + dc[d], exit_r, exit_c): # 거리가 더 가까워지면
                if board[curr_r + dr[d]][curr_c + dc[d]] == 0 or board[curr_r + dr[d]][curr_c + dc[d]] == 100: # 움직일 칸이 출구이거나 빈칸이면
                    if 0 <= curr_r + dr[d] <= N - 1 and 0 <= curr_c + dc[d] <= N - 1:  # 움직일 칸이 격자 안이면
                        dir_cand.append(d)
        # 움직일 수 있다면
        if len(dir_cand) > 0:
            dir_cand.sort()
            curr[0] += dr[dir_cand[0]]
            curr[1] += dc[dir_cand[0]]
            if board[curr[0]][curr[1]] == 100:  # 움직인 곳이 출구라면
                curr[2] = True  # 탈출
            move_cnt += 1

    return move_cnt


def rotate(grid, start_r, start_c, end_r, end_c):
    subgrid = [row[start_c:end_c+1] for row in grid[start_r:end_r+1]]
    rotated_subgrid = list(zip(*subgrid[::-1]))
    for i in range(start_r, end_r+1):
        for j in range(start_c, end_c+1):
            grid[i][j] = rotated_subgrid[i-start_r][j-start_c]


def board_rotate():
    # traveler_board 에 참가자들 정보 저장
    traveler_board = [[[] for _ in range(N)] for _ in range(N)]
    for tr_idx in range(1, len(travelers)):
        if travelers[tr_idx][2] == False:  # 아직 탈출하지 못한 참가자만 맵에 표시
            traveler_board[travelers[tr_idx][0]][travelers[tr_idx][1]].append(tr_idx)

    for size in range(2, N + 1):  # 2부터 N 까지의 사이즈 순회
        for start_row in range(0, N-size+1):
            for start_col in range(0, N-size+1):  # 시작좌표 순회

                is_exit, is_traveler = False, False
                for row in range(start_row, start_row+size):
                    for col in range(start_col, start_col+size):
                        if board[row][col] == 100:
                            is_exit = True
                        if len(traveler_board[row][col]) > 0:
                            is_traveler = True

                # 한 명 이상의 참가자와 출구를 포함
                if is_traveler and is_exit:
                    # print("회전 기준점: ", start_row, start_col, size)

                    rotate(traveler_board, start_row, start_col, start_row+size-1, start_col+size-1)
                    rotate(board, start_row, start_col, start_row+size-1, start_col+size-1)

                    # 벽 내구도 깎기
                    for i in range(start_row, start_row+size):
                        for j in range(start_col, start_col+size):
                            if board[i][j] != 100 and board[i][j] > 0:  # 벽이면
                                board[i][j] -= 1
                            if board[i][j] == 100:  # 출구면
                                global exit_r, exit_c
                                exit_r = i
                                exit_c = j

                    # traveler_board 의 정보 travelers에 다시 저장하기
                    for i in range(start_row, start_row + size):
                        for j in range(start_col, start_col + size):
                            if len(traveler_board[i][j]) > 0:  # 참가자가 있으면
                                for tr_index in traveler_board[i][j]:
                                    travelers[tr_index][0] = i
                                    travelers[tr_index][1] = j

                    # for row in traveler_board:
                    #     print(row)
                    # print()

                    return  # 이 이상 size, start_row, start_col 순회못하게 리턴해버리기



# 메인 루프
answer = 0
for turn in range(K):
    curr_score = move()
    answer += curr_score
    board_rotate()

    is_game_over = True
    for t in travelers:
        if t[0] == -1 and t[1] == -1:  # 인덱스 0번에 잇는 참여자는 허수라서 제외
            continue
        if not t[2]:
            is_game_over = False
            break

    # for row in board:
    #     print(row)
    # print()

    if is_game_over:
        break


print(answer)
print(exit_r + 1, exit_c + 1)
