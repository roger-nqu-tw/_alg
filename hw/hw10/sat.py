import numpy as np

# ==========================================
# 1. 單變數微分與積分 (數值方法)
# ==========================================
def diff_1d(f, x, h=1e-5):
    """使用中央差分法計算單變數一次微分"""
    return (f(x + h) - f(x - h)) / (2 * h)

def int_num_1d(f, a, b, bins=1000):
    """使用梯形法則計算單變數積分"""
    x = np.linspace(a, b, bins)
    y = f(x)
    return np.trapz(y, x)

# ==========================================
# 2. 單變數積分 (蒙地卡羅法)
# ==========================================
def int_mc_1d(f, a, b, n_samples=100000):
    """使用蒙地卡羅法計算單變數積分"""
    x = np.random.uniform(a, b, n_samples)
    return (b - a) * np.mean(f(x))

# ==========================================
# 3. 多變數微分(梯度) (數值方法)
# ==========================================
def grad_nd(f, x, h=1e-5):
    """計算 n 變數函數的梯度向量"""
    x = np.array(x, dtype=float)
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += h
        x_minus = x.copy()
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * h)
    return grad

# ==========================================
# 5. 黎曼積分法做 n 變數積分 (包含第3題的超體積)
# ==========================================
def integral(f, low, high, bins=None):
    """
    使用遞迴黎曼和計算 n 變數積分 (超體積)
    注意：高維度(如 100 維)會遭遇維度詛咒，bins 會動態調整
    """
    low = np.array(low, dtype=float)
    high = np.array(high, dtype=float)
    d = len(low)
    
    # 動態調整網格數以避免高維度的指數型計算爆炸
    if bins is None:
        if d == 1: bins = 1000
        elif d == 2: bins = 100
        elif d <= 5: bins = 10
        else: bins = 1  # 超高維度僅取1個切分點(區間中點)估計，否則無法算完
        
    def recurse(dim, current_x, vol):
        if dim == d:
            return f(np.array(current_x)) * vol
        
        step = (high[dim] - low[dim]) / bins
        total = 0.0
        for i in range(bins):
            mid = low[dim] + (i + 0.5) * step
            current_x.append(mid)
            total += recurse(dim + 1, current_x, vol * step)
            current_x.pop()
        return total
    
    return recurse(0, [], 1.0)

# ==========================================
# 6. 蒙地卡羅法做 n 變數積分 (包含第4題的超體積)
# ==========================================
def integral_mc(f, low, high, n_samples=100000):
    """使用蒙地卡羅法計算 n 變數積分 (超體積)"""
    low = np.array(low, dtype=float)
    high = np.array(high, dtype=float)
    d = len(low)
    
    volume = np.prod(high - low)
    # 產生形狀為 (n_samples, d) 的隨機點矩陣
    samples = np.random.uniform(low, high, (n_samples, d))
    
    # 支援未向量化的黑盒子函數，用迴圈求和
    total = np.sum([f(x) for x in samples])
    return volume * total / n_samples

# ==========================================
# 測試範例
# ==========================================
if __name__ == "__main__":
    print("=== 1 & 2. 單變數微分與積分 ===")
    f1 = lambda x: x**2
    print(f"微 分 diff_1d(x^2, 2): {diff_1d(f1, 2):.4f} (理論值: 4)")
    print(f"積 分(數值) int_num_1d:  {int_num_1d(f1, 0, 1):.4f} (理論值: 0.3333)")
    print(f"積 分(蒙地卡羅) int_mc:  {int_mc_1d(f1, 0, 1):.4f}")

    print("\n=== 3. n 變數微分 (梯度) ===")
    f_nd = lambda x: np.sum(x**2)
    print(f"grad_nd(x1^2+x2^2, [1, 2]): {grad_nd(f_nd, [1, 2])} (理論值: [2, 4])")

    print("\n=== 5 & 6. n 變數積分 (黎曼 vs 蒙地卡羅) ===")
    # 函數 f(x) = x1^2 + x2^2 + ... + xn^2
    # 積分區間 [0,1]^n 的理論值為 n / 3
    dims = [1, 2, 5, 100]
    for d in dims:
        low = [0] * d
        high = [1] * d
        exact = d / 3.0
        
        print(f"--- {d} 維積分 ---")
        print(f"理論值    : {exact:.4f}")
        
        val_riemann = integral(f_nd, low, high)
        print(f"黎曼積分  : {val_riemann:.4f}", end="")
        if d >= 100:
            print(" (因維度詛咒僅取區間中點估算)")
        else:
            print()
            
        val_mc = integral_mc(f_nd, low, high, n_samples=100000)
        print(f"蒙地卡羅  : {val_mc:.4f}")
        print("-" * 20)
