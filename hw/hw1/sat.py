    import signal
import time
import sys

N = 100          # 測試用的 n
TIMEOUT = 5      # 最長等待秒數(超過視為算不出來)
SMALL_N = 20     # 驗證正確性用的小 n

class TimeoutError(Exception):
    pass

def _handle_timeout(signum, frame):
    raise TimeoutError()

# 1. 方法 1：內建運算子
# 說明：O(1) 最快，由底層 C 語言直接計算。
def power2n_v1(n):
    return 2 ** n

# 2. 方法 2a：雙重遞迴
# 說明：O(2^n) 指數爆炸，極慢，會產生大量重複計算，大數字會卡死。
def power2n_v2a(n):
    if n == 0:
        return 1
    return power2n_v2a(n - 1) + power2n_v2a(n - 1)

# 3. 方法 2b：單一遞迴再乘 2
# 說明：O(n) 線性時間，快，但數字太大會遇到 RecursionError (遞迴深度限制)。
def power2n_v2b(n):
    if n == 0:
        return 1
    return 2 * power2n_v2b(n - 1)

# 4. 方法 3：遞迴 + 查表 (Memoization)
# 說明：O(n) 線性時間，遇到算過的值直接查表，解決 2a 的重複計算，但仍受限遞迴深度。
_table = {}
def power2n_v3(n):
    if n in _table:
        return _table[n]
    if n == 0:
        _table[0] = 1
        return 1
    _table[n] = power2n_v3(n - 1) + power2n_v3(n - 1)
    return _table[n]

# ------------------------------------------------------------
# 測試工具區塊
# ------------------------------------------------------------

# 說明：設定 timeout 秒數超時中斷，專防方法 2a 跑到卡死。
def run_with_timeout(func, n, timeout=TIMEOUT):
    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    start = time.perf_counter()
    try:
        result = func(n)
        elapsed = time.perf_counter() - start
        signal.setitimer(signal.ITIMER_REAL, 0)
        return result, elapsed, None
    except TimeoutError:
        elapsed = time.perf_counter() - start
        signal.setitimer(signal.ITIMER_REAL, 0)
        return None, elapsed, f"超過 {timeout} 秒沒算完，強制中止"

# 說明：用 n=20 檢查四種方法的答案是否都正確。
def check_correctness():
    print("=" * 60)
    print(f"正確性驗證 (n = {SMALL_N}, 期望值 = {2**SMALL_N})")
    print("=" * 60)
    expected = 2 ** SMALL_N
    results = {
        "方法1  (2**n)              ": power2n_v1(SMALL_N),
        "方法2a (遞迴+遞迴)         ": power2n_v2a(SMALL_N),
        "方法2b (遞迴*2)            ": power2n_v2b(SMALL_N),
        "方法3  (遞迴+查表)         ": power2n_v3(SMALL_N),
    }
    all_ok = True
    for name, val in results.items():
        ok = "OK" if val == expected else "FAIL"
        all_ok = all_ok and (val == expected)
        print(f"  {name} : {ok}")
    print(f"  全部正確 : {all_ok}\n")

# 說明：觀察方法 2a 隨 n 變大時，時間與次數的恐怖翻倍成長。
def growth_test_v2a():
    print("=" * 60)
    print("方法2a 成長趨勢 (證明它會指數爆炸)")
    print("=" * 60)
    for n in (10, 15, 18, 20, 22):
        _, elapsed, _ = run_with_timeout(power2n_v2a, n, timeout=5)
        calls = 2 ** (n + 1) - 1
        print(f"  n={n:>3}  呼叫次數≈2^{n+1}≈{calls:>10,} 次  花費 {elapsed:.6f} 秒")
    print()

# 說明：終極對決，在 n=100 下比較所有方法的耗時。
def compare_at_n100():
    print("=" * 60)
    print(f"效率比較 (n = {N})")
    print("=" * 60)
    v3_table_backup = dict(_table)
    _table.clear() # 測試前清空查表紀錄

    funcs = {
        "方法1 : 2**n        ": power2n_v1,
        "方法2a: 遞迴+遞迴   ": power2n_v2a,
        "方法2b: 2*遞迴      ": power2n_v2b,
        "方法3 : 遞迴+查表   ": power2n_v3,
    }

    for name, func in funcs.items():
        result, elapsed, err = run_with_timeout(func, N)
        if err is not None:
            print(f"  {name} : {err}")
        else:
            correct = (result == 2 ** N)
            print(f"  {name} : 花費 {elapsed:.6f} 秒 (正確:{correct})")

    _table.update(v3_table_backup)
    print()

if __name__ == "__main__":
    print(f"2^n 四種實作效率比較  (Python {sys.version.split()[0]})")
    check_correctness()
    growth_test_v2a()
    compare_at_n100()