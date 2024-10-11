
# 전역 변수
N, M, K = 0, 0, 0

board = []  # 총들의 정보를 기록하는 맵
players = [[-1,-1,-1,-1,0]]  # 플레이어들의 정보를 저장 [r,c,dir,stat,gun], 인덱스는 (1~M) 범위
player_score = []

# 방향 : 상우하좌
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

# 입력부
def init_input():
    global N, M, K, board, players, player_score

    N, M, K = map(int, input().split())

    # 초기화
    board = [[[] for _ in range(N)] for _ in range(N)]
    players = [[-1,-1,-1,-1,0]]
    player_score = [0 for _ in range(M+1)]

    temp_board = []
    for _ in range(N):
        temp = list(map(int, input().split()))
        temp_board.append(temp)
    for i in range(N):
        for j in range(N):
            if temp_board[i][j] > 0:
                board[i][j].append(temp_board[i][j])

    for _ in range(M):
        temp_r, temp_c, temp_dir, temp_s = map(int, input().split())
        players.append([temp_r-1, temp_c-1, temp_dir, temp_s, 0])


def is_inside(r, c):
    if 0<=r<=N-1 and 0<=c<=N-1:
        return True
    else:
        return False

# 해당 좌표에 플레이어가 있는지 없는지 확인
def is_player(r, c):
    for pidx in range(1, M+1):
        curr_r, curr_c, curr_dir, curr_stat, curr_gun = players[pidx]
        if (curr_r == r and curr_c == c):
            return True
    return False


# 해당 좌표에 있는 플레이어 인덱스 반환. 없으면 -1
def who_player(r, c):
    for pidx in range(1, M+1):
        curr_r, curr_c, curr_dir, curr_stat, curr_gun = players[pidx]
        if curr_r == r and curr_c == c:
            return pidx
    return -1


def dir_list(dir):
    arr = []
    for i in range(dir, 4):
        arr.append(i)
    for j in range(0, dir):
        arr.append(j)
    return arr



def one_round():
    # 모든 사람을 대상으로 움직임
    for pidx in range(1, M+1):
        curr_r, curr_c, curr_dir, curr_stat, curr_gun = players[pidx]

        # 1-1 해당 플레이어가 움직이게 될 좌표
        nr = curr_r + dr[curr_dir]
        nc = curr_c + dc[curr_dir]
        if not is_inside(nr, nc):
            nr = curr_r + dr[(curr_dir + 2) % 4]
            nc = curr_c + dc[(curr_dir + 2) % 4]
            players[pidx][2] = (curr_dir + 2) % 4

        # 2-1. 이동한 방향에 플레이어가 없다면
        if not is_player(nr, nc):
            # 위치 이동 시켜줌
            players[pidx][0] = nr
            players[pidx][1] = nc

            if board[nr][nc]:  # 그곳에 총이 있다면
                if curr_gun == 0:  # 플레이어가 총을 가지고 있지 않으면
                    max_gun = max(board[nr][nc])  # 놓여있는 총 중 제일 공격력이 높은 총

                    board[nr][nc].remove(max_gun)
                    players[pidx][4] = max_gun
                else:  # 플레이어가 총을 가지고 있으면
                    max_gun = max(board[nr][nc])  # 놓여있는 총 중 제일 공격력이 높은 총
                    if max_gun > curr_gun:
                        board[nr][nc].remove(max_gun)
                        board[nr][nc].append(curr_gun)
                        players[pidx][4] = max_gun


        # 2-2-1. 이동한 방향에 플레이어가 있다면
        else:
            counter_idx = who_player(nr, nc)
            counter_r, counter_c, counter_dir, counter_stat, counter_gun = players[counter_idx]

            my_num = curr_stat + curr_gun
            counter_num = counter_stat + counter_gun

            # 위치 이동 시켜줌
            players[pidx][0] = nr
            players[pidx][1] = nc

            winner_idx = -1  # 이긴 사람
            loser_idx = -1  # 진 사람
            if my_num > counter_num:
                winner_idx = pidx
                loser_idx = counter_idx
            elif my_num < counter_num:
                winner_idx = counter_idx
                loser_idx = pidx
            else:
                if curr_stat > counter_stat:
                    winner_idx = pidx
                    loser_idx = counter_idx
                else:
                    winner_idx = counter_idx
                    loser_idx = pidx

            # 이긴 플레이어 처리
            player_score[winner_idx] += abs(my_num - counter_num)

            # 2-2-2 진 플레이어 처리
            loser_r, loser_c, loser_dir, loser_stat, loser_gun = players[loser_idx]

            # 그대로 격자에 총을 내려놓기
            if loser_gun != 0:
                board[loser_r][loser_c].append(loser_gun)
                players[loser_idx][4] = 0

            # 이동
            for ldir in dir_list(loser_dir):
                loser_nr = loser_r + dr[ldir]
                loser_nc = loser_c + dc[ldir]
                if is_inside(loser_nr, loser_nc) and not is_player(loser_nr, loser_nc):  # 다른 플레이어가 없고 격자 범위 안
                    # 위치 이동 시켜줌
                    players[loser_idx][0] = loser_nr
                    players[loser_idx][1] = loser_nc
                    players[loser_idx][2] = ldir

                    if board[loser_nr][loser_nc]:  # 그곳에 총이 있다면
                        # 진 사람은 지금 무조건 총이 없음
                        max_gun = max(board[loser_nr][loser_nc])  # 놓여있는 총 중 제일 공격력이 높은 총
                        board[loser_nr][loser_nc].remove(max_gun)
                        players[loser_idx][4] = max_gun
                    # break 해줘야.
                    break

            # 2-2-3 이긴 플레이어는 승리한 칸에 떨어져 있는 총들과 원래 들고 있던 총 중 가장 공격력이 높은 총을 획득하고, 나머지 총들은 해당 격자에 내려 놓습니다.
            winner_r, winner_c, winner_dir, winner_stat, winner_gun = players[winner_idx]
            if board[winner_r][winner_c]:  # 그곳에 총이 있다면
                if winner_gun == 0:  # 플레이어가 총을 가지고 있지 않으면
                    max_gun = max(board[winner_r][winner_c])  # 놓여있는 총 중 제일 공격력이 높은 총

                    board[winner_r][winner_c].remove(max_gun)
                    players[winner_idx][4] = max_gun
                else:  # 플레이어가 총을 가지고 있으면
                    max_gun = max(board[winner_r][winner_c])  # 놓여있는 총 중 제일 공격력이 높은 총
                    if max_gun > winner_gun:
                        board[winner_r][winner_c].remove(max_gun)
                        board[winner_r][winner_c].append(winner_gun)
                        players[winner_idx][4] = max_gun


# 메인 루프
T = int(input())
for tc in range(T):
    init_input()
    for r in range(K):
        one_round()
    for i in range(1, M + 1):
        print(player_score[i], end=" ")
    print()




"""
느낀점:
1. 플레이어를 이동시키고 나서, 이동한 플레이어를 중복 처리하지는 않았는지 꼭 체크!

ex)
# 모든 사람을 대상으로 움직임
    for pidx in range(1, M+1):
        curr_r, curr_c, curr_dir, curr_stat, curr_gun = players[pidx]

        # 1-1 해당 플레이어가 움직이게 될 좌표
        nr = curr_r + dr[curr_dir]
        nc = curr_c + dc[curr_dir]
        if not is_inside(nr, nc):
            nr = curr_r + dr[(curr_dir + 2) % 4]
            nc = curr_c + dc[(curr_dir + 2) % 4]
            players[pidx][2] = (curr_dir + 2) % 4
        
        # 위치 이동 시켜줌
        players[pidx][0] = nr
        players[pidx][1] = nc

        # 2-1. 이동한 방향에 플레이어가 없다면
        if not is_player(nr, nc):
            
=> 위 같은 경우에는 nr, nc로 이동을 처리해주고 나서, is_player(nr, nc)를 통해 해당 좌표에 플레이어가 있는지 찾았는데,
   이렇게 되면 방금전에 움직인 자기 자신이 is_player(nr, nc)에 걸리게 되는 것. 
   
   
2. 실제 시험환경 처럼 여러 tc를 반복문으로 돌려보는 연습 해봄. 
"""