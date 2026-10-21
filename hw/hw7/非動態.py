def is_match_nfa(s: str, p: str) -> bool:
    """用狀態集合模擬 Thompson NFA (不建複雜圖結構，直接以模式索引 j 作為狀態編號)"""
    n = len(p)

    def get_epsilon_closure(states: set) -> set:
        """計算 epsilon 閉包：遇到 x* 可以不消耗字元直接跳到 j+2"""
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            # 如果下一個字元是 '*'，代表當前可經由 epsilon 轉移跳過 'x*'
            if state + 1 < n and p[state + 1] == '*':
                if (state + 2) not in closure:
                    closure.add(state + 2)
                    stack.append(state + 2)
        return closure

    # 初始狀態為 0 的 epsilon 閉包
    current_states = get_epsilon_closure({0})

    # 逐字元推進狀態機
    for char in s:
        next_states = set()
        for state in current_states:
            if state < n:
                # 若下一個是 '*'，匹配成功後仍停留在當前 state (代表可重複匹配)
                if state + 1 < n and p[state + 1] == '*':
                    if p[state] in {char, '.'}:
                        next_states.add(state)
                # 一般字元匹配成功，推進到 state + 1
                elif p[state] in {char, '.'}:
                    next_states.add(state + 1)
        # 展開新狀態集合的 epsilon 閉包
        current_states = get_epsilon_closure(next_states)
        if not current_states:
            return False  # 所有可能分支皆死亡，提早結束

    # 檢查終點狀態 n 是否在活躍狀態集合中
    return n in current_states