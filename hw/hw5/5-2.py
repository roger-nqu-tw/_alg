def sym_diff(expr, var='x'):
    """
    使用遞迴進行符號微分
    expr: 表示數學式的 Tuple 或基本型別 (int, float, str)
    var: 對哪一個變數進行微分 (預設為 'x')
    """
    # 1. 基本情況：常數 (整數或浮點數)
    if isinstance(expr, (int, float)):
        return 0
        
    # 2. 基本情況：變數 (字串)
    if isinstance(expr, str):
        return 1 if expr == var else 0

    # 3. 遞迴情況：解析運算子與運算元
    op = expr[0]
    
    if op == '+':
        u, v = expr[1], expr[2]
        return ('+', sym_diff(u, var), sym_diff(v, var))
        
    elif op == '-':
        u, v = expr[1], expr[2]
        return ('-', sym_diff(u, var), sym_diff(v, var))
        
    elif op == '*':
        u, v = expr[1], expr[2]
        # 乘法法則：u'v + uv'
        return ('+', 
                ('*', sym_diff(u, var), v), 
                ('*', u, sym_diff(v, var)))
                
    elif op == '/':
        u, v = expr[1], expr[2]
        # 除法法則：(u'v - uv') / (v*v)
        return ('/', 
                ('-', ('*', sym_diff(u, var), v), ('*', u, sym_diff(v, var))), 
                ('*', v, v))
                
    elif op == '^':
        u, n = expr[1], expr[2]
        # 次方法則：n * u^(n-1) * u'
        return ('*', 
                ('*', n, ('^', u, n - 1)), 
                sym_diff(u, var))
                
    else:
        raise ValueError(f"未知的運算子: {op}")

# 輔助函數：將 Tuple 格式的數學式轉回可讀字串
def expr_to_str(expr):
    if isinstance(expr, (int, float, str)):
        return str(expr)
    op, u, v = expr[0], expr[1], expr[2]
    return f"({expr_to_str(u)} {op} {expr_to_str(v)})"

# === 測試與執行範例 ===

# 測試式子 1: f(x) = x^2 + 3*x
# 結構為: ('+', ('^', 'x', 2), ('*', 3, 'x'))
f1 = ('+', ('^', 'x', 2), ('*', 3, 'x'))
df1 = sym_diff(f1, 'x')

print(f"原式 f(x) = {expr_to_str(f1)}")
print(f"微分 f'(x) = {expr_to_str(df1)}")
# 注意：程式會輸出未化簡的結果，例如 ((2 * (x ^ 1)) * 1) + ((0 * x) + (3 * 1))