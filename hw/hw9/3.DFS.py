def solve_n_queens(n):
    def dfs(queens, xy_dif, xy_sum):
        p = len(queens)
        if p == n:
            result.append(queens)
            return
        for q in range(n):
            if q not in queens and p - q not in xy_dif and p + q not in xy_sum:
                dfs(queens + [q], xy_dif + [p - q], xy_sum + [p + q])
    result = []
    dfs([], [], [])
    return result