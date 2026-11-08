def solve_maze(maze, x, y, dest_x, dest_y, path):
    if x == dest_x and y == dest_y:
        path.append((x, y))
        return True
    if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] == 0:
        maze[x][y] = 2  # 標記為已訪問
        path.append((x, y))
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if solve_maze(maze, x + dx, y + dy, dest_x, dest_y, path):
                return True
        path.pop()
    return False