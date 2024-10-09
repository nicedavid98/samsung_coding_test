from copy import deepcopy

dr = [-1,-1,0,1,1,1,0,-1]
dc = [0,-1,-1,-1,0,1,1,1]

monster_map = [[[0,0,0,0,0,0,0,0] for _ in range(4)] for _ in range(4)]  # 살아있는 몬스터만 기록하는 맵
egg_map = [[[0,0,0,0,0,0,0,0] for _ in range(4)] for _ in range(4)]  # 알 상태의 몬스터만 기록하는 맵
dead_map = [[[] for _ in range(4)] for _ in range(4)] #  시체를 모아놓은 맵

packman_move_list = []
def permutation(length, new_arr, depth):
    arr = [0,2,4,6]
    if len(new_arr) == length:
        packman_move_list.append(new_arr)
        return
    for i in range(0, 4):
        permutation(length, new_arr + [arr[i]], depth + 2)
permutation(3, [], 0)


# 입력부
m, t = map(int, input().split())
packman_r, packman_c = map(int, input().split())
packman_r -= 1
packman_c -= 1
for _ in range(m):
    r, c, d = map(int, input().split())
    monster_map[r-1][c-1][d-1] += 1


def counterclockwise_arr(dir):
    arr =[]
    for i in range(dir, 8):
        arr.append(i)
    for j in range(0, dir):
        arr.append(j)
    return arr


def count_monsters(r, c):
    cnt = 0
    for idx in range(8):
        cnt += monster_map[r][c][idx]
    return cnt


def print_monster_map():
    temp = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            temp[i][j] = count_monsters(i, j)
    for row in temp:
        print(row)
    print()


def duplicate():
    for i in range(4):
        for j in range(4):
           for idx in range(8):
               egg_map[i][j][idx] += monster_map[i][j][idx]


def monster_move():
    migrated_monster_map = [[[0,0,0,0,0,0,0,0] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for idx in range(8):
                if monster_map[i][j][idx] > 0:  # 해당 방향에 몬스터가 있다면
                    counter_arr = counterclockwise_arr(idx)
                    for dir in counter_arr:
                        nr = i + dr[dir]
                        nc = j + dc[dir]
                        if 0<=nr<=3 and 0<=nc<=3 and not (nr == packman_r and nc == packman_c) and len(dead_map[nr][nc]) == 0:  # 해당 방향으로 이동 가능
                            migrated_monster_map[nr][nc][dir] += monster_map[i][j][idx]
                            monster_map[i][j][idx] = 0
                            break

    for i in range(4):
        for j in range(4):
            for idx in range(8):
                monster_map[i][j][idx] += migrated_monster_map[i][j][idx]


def packman_move(turn):
    global packman_r, packman_c
    eat_count = [0 for _ in range(len(packman_move_list))]
    for idx in range(len(packman_move_list)):
        visited = [[False for _ in range(4)] for _ in range(4)]
        cnt = 0
        cr = packman_r
        cc = packman_c
        can_move = True
        for dir in packman_move_list[idx]:
            nr = cr + dr[dir]
            nc = cc + dc[dir]
            if 0<=nr<=3 and 0<=nc<=3:
                if visited[nr][nc] == False:
                    cnt += count_monsters(nr, nc)
                visited[nr][nc] = True
                cr = nr
                cc = nc
            else:
                can_move = False
                break
        if can_move:
            eat_count[idx] = cnt

    max_count = max(eat_count)

    move_idx = -1  # 움직일 방법을 정함.
    for i in range(len(eat_count)):
        if max_count == eat_count[i]:
            move_idx = i
            break

    curr_r = packman_r
    curr_c = packman_c
    for dir in packman_move_list[move_idx]:
        curr_r += dr[dir]
        curr_c += dc[dir]
        # 몬스터 맵에 있던 놈을을 시체방으로 옮기기
        if count_monsters(curr_r, curr_c) > 0:
            monster_map[curr_r][curr_c] = [0,0,0,0,0,0,0,0]
            dead_map[curr_r][curr_c].append(turn + 2)

    packman_r = curr_r
    packman_c = curr_c


def dead_clear(turn):
    for i in range(4):
        for j in range(4):
            dead_map[i][j] = list(set(dead_map[i][j]))  # 중복 제거
            if turn in dead_map[i][j]:
                dead_map[i][j].remove(turn)


def egg_born():
    for i in range(4):
        for j in range(4):
            for idx in range(8):
                monster_map[i][j][idx] += egg_map[i][j][idx]
                egg_map[i][j][idx] = 0


# 메인 루프
for turn in range(t):
    duplicate()
    # print_monster_map()

    monster_move()
    # print_monster_map()

    packman_move(turn)
    # print_monster_map()

    dead_clear(turn)
    egg_born()
    # print_monster_map()


answer = 0
for i in range(4):
    for j in range(4):
        answer += count_monsters(i, j)
print(answer)



"""
느낀 점 

1. monster_move() 
격자를 순회하는 방식으로 무언가(몬스터)를 순회하면서 움직여 주어야 할때
=> 몬스터가 움직임으로 인해 (당연히 격자에 기록되겠지), 격자를 순회할 때 중복 처리가 될 수 있음을 유의. 
=> 이럴 때는 빈 격자를 하나 가져와서 거기다가 움직인 놈들을 집어놓고, 원래 격자에는 없애버리는 방식으로 해결 가능

2. monster_move()
움직인 몬스터의 방향이 바뀌었을 때, 그거 꼭 처리해주기 

3. cr,cc와 nr,nc 구별 잘하기 
if 0<=nr<=3 and 0<=nc<=3 and not (nr == packman_r and nc == packman_c) and len(dead_map[nr][nc]) == 0:
이거를 
if 0<=nr<=3 and 0<=nc<=3 and not (nr == packman_r and nc == packman_c) and len(dead_map[i][j]) == 0:
로 써서 디버깅 힘들었음

4. 조합 함수 구현방법


"""



