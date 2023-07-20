def countdown(n):
    while n > 0:
        yield n
        n -= 1

p = countdown(5)  # 创建生成器对象
print(p)  # 输出: 5
print(next(p))  # 输出: 4
print(next(p))  # 输出: 3
print(next(p))  # 输出: 2
print(next(p))  # 输出: 1

