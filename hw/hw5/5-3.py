// 1. 自製 map (使用遞迴)
const myMap = (arr, fn) => {
    if (arr.length === 0) return [];
    const [head, ...tail] = arr; // 陣列解構：取出首項與剩餘陣列
    return [fn(head), ...myMap(tail, fn)];
};

// 2. 自製 filter (使用遞迴)
const myFilter = (arr, fn) => {
    if (arr.length === 0) return [];
    const [head, ...tail] = arr;
    return fn(head) 
        ? [head, ...myFilter(tail, fn)] 
        : myFilter(tail, fn);
};

// 3. 自製 reduce (使用遞迴)
const myReduce = (arr, fn, initialValue) => {
    if (arr.length === 0) return initialValue;
    const [head, ...tail] = arr;
    
    // 若沒有提供初始值，以陣列第一個元素作為初始值繼續遞迴
    if (initialValue === undefined) {
        return myReduce(tail, fn, head);
    }
    return myReduce(tail, fn, fn(initialValue, head));
};

// 4. 無迴圈泡沫排序 (Bubble Sort)
const bubbleSort = (arr) => {
    // 終止條件：當陣列長度 <= 1 時，自然已排序完成
    if (arr.length <= 1) return arr;

    const [head, ...tail] = arr;

    // 執行一次 Bubble Pass (內層迴圈)：利用 myReduce 將最大值推到最後
    const { res, max } = myReduce(tail, (acc, curr) => {
        if (acc.max > curr) {
            // 目前記錄的最大值仍大於當前元素 -> 將當前元素留在剩餘陣列，max 繼續往右比較
            return { res: [...acc.res, curr], max: acc.max };
        } else {
            // 當前元素較大 -> 將原本的 max 留在剩餘陣列，當前元素成為新的 max
            return { res: [...acc.res, acc.max], max: curr };
        }
    }, { res: [], max: head });

    // 遞迴呼叫 (外層迴圈)：對剩餘未完全排序的陣列 (res) 繼續泡沫排序，最後接上這次遍歷得到的最大值 (max)
    return [...bubbleSort(res), max];
};

// ================= 測試區 =================

const data = [5, 3, 8, 4, 1, 9, 2];

console.log("【排序測試】");
console.log("原始陣列:", data);
console.log("泡沫排序後:", bubbleSort(data)); 
// 輸出: [1, 2, 3, 4, 5, 8, 9]

console.log("\n【自製函數測試】");
console.log("myMap (* 2):", myMap(data, x => x * 2)); 
// 輸出: [10, 6, 16, 8, 2, 18, 4]

console.log("myFilter (> 4):", myFilter(data, x => x > 4)); 
// 輸出: [5, 8, 9]

console.log("myReduce (加總):", myReduce(data, (a, b) => a + b, 0)); 
// 輸出: 32