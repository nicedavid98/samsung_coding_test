

arr = [0,1,2,3]

# 중복 순열
def product(length, new_arr):
    if len(new_arr) == length:
        print(new_arr)
        return
    for i in range(0 ,len(arr)):
        product(length, new_arr + [arr[i]])

product(3, [])


# for dir in range(2, 8):
#     print(dir)
# for dir in range(0, 2):
#     print(dir)