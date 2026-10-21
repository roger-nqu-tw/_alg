def is_match_dp(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    # dp[i][j] 表示 s[:i] 與 p[:j] 是否匹配
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True  # 空字串與空模式必匹配

    # 初始化：處理 s 為空字串，但 p 為 "a*b*c*" 等可消去為空的情況
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]

    # 填表過程
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # 情況 1: '*' 匹配 0 次 (跳過 p[j-2] 與 '*')
                dp[i][j] = dp[i][j - 2]
                # 情況 2: '*' 匹配 1 次以上 (需 s[i-1] 與 p[j-2] 匹配)
                if p[j - 2] == s[i - 1] or p[j - 2] == '.':
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            else:
                # 一般字元或 '.' 的直接比對
                if p[j - 1] == s[i - 1] or p[j - 1] == '.':
                    dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]