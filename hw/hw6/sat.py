import re

# ==========================================
# 1. 抽象語法樹 (AST)
# ==========================================
class Term:
    pass

class Var(Term):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class Abs(Term):
    def __init__(self, param, body):
        self.param = param
        self.body = body
    def __str__(self):
        return f"(λ{self.param}.{self.body})"

class App(Term):
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg
    def __str__(self):
        return f"({self.func} {self.arg})"

# ==========================================
# 2. 核心運算邏輯 (自由變數、替換、Alpha轉換)
# ==========================================
def free_vars(term):
    """取得表示式中的自由變數"""
    if isinstance(term, Var):
        return {term.name}
    elif isinstance(term, Abs):
        return free_vars(term.body) - {term.param}
    elif isinstance(term, App):
        return free_vars(term.func) | free_vars(term.arg)

def substitute(term, x, N):
    """將 term 中的自由變數 x 替換為 N (Capture-avoiding substitution)"""
    if isinstance(term, Var):
        return N if term.name == x else term
    
    elif isinstance(term, App):
        return App(substitute(term.func, x, N), substitute(term.arg, x, N))
    
    elif isinstance(term, Abs):
        if term.param == x:
            return term # 變數被遮蔽 (Shadowed)
        
        if term.param in free_vars(N):
            # 發生變數捕捉，進行 Alpha 轉換 (重新命名)
            new_param = term.param + "'"
            while new_param in free_vars(term.body) | free_vars(N):
                new_param += "'"
            # 先把本體裡的舊參數換成新參數，再進行外部的替換
            new_body = substitute(term.body, term.param, Var(new_param))
            return Abs(new_param, substitute(new_body, x, N))
        else:
            return Abs(term.param, substitute(term.body, x, N))

def reduce_step(term):
    """執行一步 Normal-order 歸約 (從左到右，最外層優先)"""
    if isinstance(term, Var):
        return term, False
    
    elif isinstance(term, Abs):
        new_body, reduced = reduce_step(term.body)
        return Abs(term.param, new_body), reduced
    
    elif isinstance(term, App):
        if isinstance(term.func, Abs):
            # 找到 Redex！執行 Beta 歸約：(\x.M) N  ->  M[x := N]
            return substitute(term.func.body, term.func.param, term.arg), True
        else:
            # 嘗試歸約左邊的函數
            new_func, reduced = reduce_step(term.func)
            if reduced:
                return App(new_func, term.arg), True
            # 左邊無法歸約，嘗試歸約右邊的參數
            new_arg, reduced = reduce_step(term.arg)
            return App(term.func, new_arg), reduced

# ==========================================
# 3. 語法解析與巨集展開 (Parser)
# ==========================================
def tokenize(code):
    code = code.replace('\\', 'λ') # 支援 \x.x 與 λx.x
    tokens = re.findall(r'λ|\.|[a-zA-Z0-9_]+|\(|\)', code)
    return tokens

def parse(tokens):
    def parse_term(tokens):
        if not tokens: return None
        if tokens[0] == 'λ':
            tokens.pop(0) # 移除 λ
            param = tokens.pop(0)
            tokens.pop(0) # 移除 .
            body = parse_term(tokens)
            return Abs(param, body)
        else:
            # 處理連續的應用 (Application) e.g., M N P -> ((M N) P)
            nodes = []
            while tokens and tokens[0] not in (')', 'λ', '.'):
                if tokens[0] == '(':
                    tokens.pop(0) # 移除 (
                    nodes.append(parse_term(tokens))
                    tokens.pop(0) # 移除 )
                else:
                    nodes.append(Var(tokens.pop(0)))
            
            if not nodes: return None
            term = nodes[0]
            for n in nodes[1:]:
                term = App(term, n)
            return term
    return parse_term(tokens)

def expand_macros(term, env):
    """將 AST 中的具名巨集 (如 TRUE, AND) 展開成實際的 Lambda 表示式"""
    if isinstance(term, Var):
        if term.name in env:
            # 解析並展開巨集
            return expand_macros(parse(tokenize(env[term.name])), env)
        return term
    elif isinstance(term, Abs):
        return Abs(term.param, expand_macros(term.body, env))
    elif isinstance(term, App):
        return App(expand_macros(term.func, env), expand_macros(term.arg, env))

# ==========================================
# 4. 執行與顯示介面
# ==========================================
def evaluate(code, env=None):
    if env is None: env = {}
    print(f"\n[輸入] {code}")
    
    tokens = tokenize(code)
    ast = parse(tokens)
    ast = expand_macros(ast, env)
    
    print(f"[展開] {ast}")
    
    step = 0
    current_term = ast
    while True:
        next_term, reduced = reduce_step(current_term)
        if not reduced:
            break
        step += 1
        print(f"Step {step}: {next_term}")
        current_term = next_term
        
    print(f"[最終結果] {current_term}\n" + "-"*40)

# ==========================================
# 5. 測試程式碼
# ==========================================
if __name__ == "__main__":
    # 定義具名巨集 (環境字典)
    env = {
        # 布林邏輯
        "TRUE":  "λx.λy.x",
        "FALSE": "λx.λy.y",
        "AND":   "λp.λq.p q p",
        "OR":    "λp.λq.p p q",
        "NOT":   "λp.λa.λb.p b a",
        
        # 邱奇數 (Church Numerals)
        "ZERO":  "λf.λx.x",
        "ONE":   "λf.λx.f x",
        "TWO":   "λf.λx.f (f x)",
        "SUCC":  "λn.λf.λx.f (n f x)",
        "ADD":   "λm.λn.λf.λx.m f (n f x)"
    }

    # 測試 1: 簡單的替換與應用
    evaluate(r"(\x. x) y")
    
    # 測試 2: 變數捕捉測試 (會自動觸發 Alpha 轉換，將內部的 y 改為 y')
    evaluate(r"(\x. \y. x) y")

    # 測試 3: 布林邏輯 (AND TRUE FALSE -> FALSE)
    evaluate("AND TRUE FALSE", env)

    # 測試 4: 布林邏輯 (NOT TRUE -> FALSE)
    evaluate("NOT TRUE", env)

    # 測試 5: 數學運算 (SUCC ONE -> TWO 的結構)
    evaluate("SUCC ONE", env)

    # 測試 6: 數學運算 (ADD ONE ONE)
    evaluate("ADD ONE ONE", env)