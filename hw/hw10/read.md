# 數值微積分與蒙地卡羅積分 (Numerical & Monte Carlo Calculus)

本專案實作了幾何、物理以及機器學習領域中常見的微積分數值算法。主要包含「單變數」與「多變數 (n維)」的微分與積分，並實作傳統的「網格切分法 (黎曼積分)」與以隨機採樣為基礎的「蒙地卡羅法」。

## 功能清單 (Features)

1. **單變數數值微分**：採用中央差分法 (Central Difference)。
2. **單變數數值積分**：採用梯形法則 (Trapezoidal Rule)。
3. **單變數蒙地卡羅積分**：藉由均勻分布的亂數採樣與期望值計算定積分。
4. **多變數數值梯度**：計算多變數函數的偏導數向量 (Gradient)。
5. **多變數黎曼積分 (`integral`)**：使用遞迴的方式對空間做網格切分計算超體積。具備防呆機制，根據維度自動下修 `bins` 數量以防止記憶體溢出。
6. **多變數蒙地卡羅積分 (`integral_mc`)**：突破高維度計算瓶頸，實作快速估計。

## 執行與測試

1. **自動測試**：直接執行本 Python 腳本將會自動跑完全部的測試範例。
```bash
python calc_methods.py
```
2. **自訂測試與引入**：您可以輕易地將這些函數引入您的專案中。
```python
import numpy as np
from calc_methods import integral_mc, grad_nd

# 定義一個任意的 3 變數函數 f(x, y, z)
def my_func(x):
    return x[0] * np.sin(x[1]) + np.exp(x[2])

# 計算梯度 (在點 [1, 0, 1])
gradient = grad_nd(my_func, [1, 0, 1])
print(f"Gradient: {gradient}")

# 使用蒙地卡羅法估計該函數在 [0,1]x[0,2]x[0,1] 範圍內的 3 維積分
result = integral_mc(my_func, low=[0, 0, 0], high=[1, 2, 1], n_samples=50000)
print(f"Monte Carlo Integration: {result:.4f}")
```

## 數學原理與演算法詳解

1. **數值微分 (Numerical Differentiation)**：在無法取得函數解析解（Analytical solution）時，我們可以使用有限差分來逼近導數。採用**中央差分法 (Central Difference)**，其截斷誤差為 $O(h^2)$，公式如下：
$$f'(x) \approx \frac{f(x + h) - f(x - h)}{2h}$$
對於多變數函數的梯度 $\nabla f$，我們對向量 $\mathbf{x} = [x_1, x_2, \dots, x_n]$ 中的每一個維度分別進行中央差分來求得偏導數：
$$\frac{\partial f}{\partial x_i} \approx \frac{f(x_1, \dots, x_i + h, \dots) - f(x_1, \dots, x_i - h, \dots)}{2h}$$

2. **數值積分網格法 (Grid-based Integration)**：透過將積分區間切割成許多微小的子區間，並計算每個子區間的面積/體積總和來逼近真實積分值。單變數利用**梯形法則**：
$$\int_{a}^{b} f(x) dx \approx \sum_{i=1}^{N} \frac{f(x_{i-1}) + f(x_i)}{2} \Delta x$$
**維度詛咒 (Curse of Dimensionality)**：多變數黎曼積分在 $d$ 維空間中，若每個維度切割 $k$ 等分，總共需要計算的網格點數目為 $k^d$。這會導致計算時間呈指數級爆炸。為避免記憶體耗盡，本專案程式碼在 `d > 5` 時會自動降級網格數。

3. **蒙地卡羅積分 (Monte Carlo Integration)**：蒙地卡羅法不依賴網格，而是依賴**大數法則 (Law of Large Numbers)**，透過隨機採樣來估計積分值。將積分視為函數在該區域上的**平均高度**乘以**區域總底面積 (超體積 $V$)**：
$$
\int_{V} f(\mathbf{x}) d\mathbf{x} \approx V \times \frac{1}{N} \sum_{i=1}^{N} f(\mathbf{x}_i)
$$
無論維度 $d$ 有多高，蒙地卡羅法的誤差收斂速度始終與 $O(1/\sqrt{N})$ 成正比，這使其成為解決高維度積分的最佳方案。

## 測試案例解析：決戰 100 維

我們使用了以下函數進行 $n$ 變數積分測試，積分範圍落在單位超立方體 $[0, 1]^n$ 內，其理論值推導為 $\frac{n}{3}$：
$$
f(\mathbf{x}) = x_1^2 + x_2^2 + \dots + x_n^2 = \sum_{i=1}^{n} x_i^2
$$
當測試維度高達 **100 維** 時 (理論值為 $33.3333$)：

1. **黎曼積分測試 (Riemann)**：由於 $O(k^{100})$ 帶來的「維度詛咒」，如果每維度僅切 2 刀，計算量為 $2^{100} \approx 1.26 \times 10^{30}$ 次。程式為防止當機自動退化為僅採樣 1 刀 (取中點估計)，結果為 `25.0`，誤差極大。
2. **蒙地卡羅法測試 (Monte Carlo)**：只要給定 $100,000$ 個高維度隨機樣本點，瞬間即可給出極度接近 `33.33` 的結果，完美展示了其在超高維度運算中不可替代的優勢。
