
##遞迴

def hanoi(n, source, target, auxiliary):
    """
    n: 盤子數量
    source: 起始柱
    target: 目標柱
    auxiliary: 暫存輔助柱
    """
    # Base Case (終止條件)：當只有一個盤子時，不需要輔助柱，直接將其從起點移到終點
    if n == 1:
        print(f"將盤子 1 從 {source} 移動到 {target}")
        return

    # 步驟一：將上方的 n-1 個盤子從起點 (source) 移到暫存柱 (auxiliary)
    # 這裡將終點 (target) 當作輔助柱來借放
    hanoi(n - 1, source, auxiliary, target)

    # 步驟二：此時 source 上只剩下最大的第 n 個盤子，直接將它移到終點 (target)
    print(f"將盤子 {n} 從 {source} 移動到 {target}")

    # 步驟三：將剛剛暫放在暫存輔助柱 (auxiliary) 的 n-1 個盤子移到終點 (target)
    # 這裡將原本的起點 (source) 當作輔助柱來借放
    hanoi(n - 1, auxiliary, target, source)

# 測試執行：3 個盤子，A為起點，C為終點，B為暫存柱
hanoi(3, 'A', 'C', 'B')


##非遞迴

def hanoi_iterative(n, source='A', target='C', aux='B'):
    # 總移動次數為 2^n - 1
    total_moves = (1 << n) - 1 
    
    # 建立三根柱子的堆疊，將盤子由大到小放入 A 柱
    # 假設 n=3，stack_A 會是 [3, 2, 1]，數字越小代表盤子越小
    stack_A = [i for i in range(n, 0, -1)] 
    stack_B = []
    stack_C = []
    
    # 如果盤子數量是偶數，將目標柱與輔助柱的角色對調
    if n % 2 == 0:
        target, aux = aux, target
        stack_C, stack_B = stack_B, stack_C

    def move_legal(peg1, peg2, name1, name2):
        """在兩根柱子之間進行唯一合法的移動"""
        if not peg1:  # peg1 為空，只能把 peg2 移過來
            peg1.append(peg2.pop())
            print(f"移動盤子 {peg1[-1]} 從 {name2} 到 {name1}")
        elif not peg2: # peg2 為空，只能把 peg1 移過來
            peg2.append(peg1.pop())
            print(f"移動盤子 {peg2[-1]} 從 {name1} 到 {name2}")
        elif peg1[-1] > peg2[-1]: # peg2 的頂端盤子較小，移到 peg1 上
            peg1.append(peg2.pop())
            print(f"移動盤子 {peg1[-1]} 從 {name2} 到 {name1}")
        else: # peg1 的頂端盤子較小，移到 peg2 上
            peg2.append(peg1.pop())
            print(f"移動盤子 {peg2[-1]} 從 {name1} 到 {name2}")

    # 執行迴圈，處理所有步驟
    for i in range(1, total_moves + 1):
        if i % 3 == 1:
            move_legal(stack_A, stack_C, source, target)
        elif i % 3 == 2:
            move_legal(stack_A, stack_B, source, aux)
        elif i % 3 == 0:
            move_legal(stack_B, stack_C, aux, target)

# 測試執行：3 個盤子
print("迭代法河內塔移動步驟：")
hanoi_iterative(3)