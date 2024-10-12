
pos_arr = [[0,1], [1,1], [3,1], [4,0], [5,4], [0,0], [0, 9]]

pos_arr.sort(key=lambda x: (-x[0], x[1]))
print(pos_arr)

# 키는람다X: ()