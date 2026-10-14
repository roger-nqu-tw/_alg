# 這是如何運作的？
##　語法 (Syntax)：

支援 \ 或 λ 作為 Lambda 符號。例如 \x.\y.x 與 λx.λy.x 是等價的。

會自動處理左結合的函數應用（Application），例如 M N P 會被解析為 ((M N) P)。

## 具名環境 (Named Environment)：
我在 env 字典中定義了標準的 Lambda Calculus 程式館。你輸入 AND TRUE FALSE 時，Parser 會將 AND、TRUE、FALSE 替換為對應的 Lambda 本體，再開始計算。

## 計算過程 (Beta Reduction)：
每次遇到 (λx. M) N 的結構，解譯器會將 M 裡面的自由變數 x 替換為 N，並確保不發生變數捕捉（如果發生，會把變數重新命名成 y'）。