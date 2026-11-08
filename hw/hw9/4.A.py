import heapq

def a_star_search(grid, start, goal):
    def heuristic(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    front = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while front:
        _, current = heapq.heappop(front)
        if current == goal: break
        
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            next_node = (current[0] + dx, current[1] + dy)
            if 0 <= next_node[0] < len(grid) and 0 <= next_node[1] < len(grid[0]) and grid[next_node[0]][next_node[1]] == 0:
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(front, (priority, next_node))
                    came_from[next_node] = current
    return came_from