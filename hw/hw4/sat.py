# 定義極簡的迭代函數
g = lambda x: 1 + 1 / x

# 從 1.0 開始猜
x = 1.0

for i in range(10):
    x = g(x)
    print(f"第 {i+1:<2} 次: {x:.6f}")
