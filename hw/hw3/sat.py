程式還在修改
import itertools

def solve_sat_by_truth_table(variables, formula_func):
    """
    透過完整列舉真質表來解決 SAT 問題。
    
    :param variables: 變數名稱的列表，例如 ['A', 'B', 'C']
    :param formula_func: 接收一個字典（變數映射）並回傳布林值的函式
    """
    n = len(variables)
    satisfying_assignments = []
    
    # 建立真質表的標頭
    header = " | ".join(variables) + " || Result"
    print(header)
    print("-" * len(header))
    
    # itertools.product 會生成所有 2^n 種 True/False 的組合
    # 例如：(False, False), (False, True), (True, False), (True, True)...
    for combination in itertools.product([False, True], repeat=n):
        # 將變數名稱與目前的 True/False 組合配對成字典
        # 例如：{'A': False, 'B': True, 'C': False}
        env = dict(zip(variables, combination))
        
        # 將這組設定代入方程式計算結果
        result = formula_func(env)
        
        # 格式化輸出，將 True 轉為 'T'，False 轉為 'F' 方便閱讀
        row_str = " | ".join(["T" if val else "F" for val in combination])
        res_str = "T" if result else "F"
        print(f"{row_str} ||   {res_str}")
        
        # 如果結果為 True，記錄這組解
        if result:
            satisfying_assignments.append(env)
            
    return satisfying_assignments

# ==========================================
# 測試範例：(A ∨ B) ∧ (¬A ∨ C) ∧ (¬B ∨ ¬C)
# ==========================================
def my_formula(env):
    A = env['A']
    B = env['B']
    C = env['C']
    return (A or B) and (not A or C) and (not B or not C)

if __name__ == "__main__":
    variables = ['A', 'B', 'C']
    
    print("開始分析方程式：(A or B) and (not A or C) and (not B or not C)\n")
    solutions = solve_sat_by_truth_table(variables, my_formula)
    
    print("\n--- 分析結果 ---")
    if solutions:
        print(f"此方程式為【可滿足 (Satisfiable)】！共找到 {len(solutions)} 組解：")
        for i, sol in enumerate(solutions, 1):
            print(f"解 {i}: {sol}")
    else:
        print("此方程式為【不可滿足 (Unsatisfiable)】。")
