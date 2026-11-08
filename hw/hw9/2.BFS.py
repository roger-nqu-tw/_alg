from collections import deque

def is_valid(state):
    f, w, g, c = state
    if w == g and f != w: return False # 狼吃羊
    if g == c and f != g: return False # 羊吃菜
    return True

def solve_river_crossing():
    start, goal = (0, 0, 0, 0), (1, 1, 1, 1)
    queue = deque([(start, [])])
    visited = set([start])
    
    while queue:
        state, path = queue.popleft()
        if state == goal: return path + [state]
        
        f, w, g, c = state
        next_f = 1 - f
        moves = [(next_f, w, g, c), (next_f, next_f, g, c), (next_f, w, next_f, c), (next_f, w, g, next_f)]
        
        for next_state in moves:
            if is_valid(next_state) and next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [state]))