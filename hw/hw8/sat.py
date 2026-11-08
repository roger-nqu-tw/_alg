import numpy as np
import random
import math

# 設定隨機種子以利重現結果，並生成 10 個城市的 2D 座標
np.random.seed(42)
cities = np.random.rand(10, 2)
num_cities = len(cities)

def calc_total_dist(route):
    """計算給定路徑的總歐幾里得距離（包含回到起點）"""
    dist = 0.0
    for i in range(len(route)):
        c1 = cities[route[i]]
        c2 = cities[route[(i + 1) % len(route)]]
        dist += np.linalg.norm(c1 - c2)
    return dist

# 隨機初始解
initial_route = list(range(num_cities))
random.shuffle(initial_route)

"1."
def two_opt(route):
    best_route = route.copy()
    improved = True
    
    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                # 反轉 i 到 j 之間的路徑
                new_route = best_route.copy()
                new_route[i:j] = best_route[i:j][::-1]
                
                if calc_total_dist(new_route) < calc_total_dist(best_route):
                    best_route = new_route
                    improved = True
                    # 找到改良即重新開始掃描
                    break
            if improved:
                break
                
    return best_route

print("2-opt 距離:", calc_total_dist(two_opt(initial_route)))

"2."
def hill_climbing(route):
    current_route = route.copy()
    
    while True:
        best_neighbor = None
        best_dist = calc_total_dist(current_route)
        
        # 產生所有鄰居並找出最佳者
        for i in range(len(route)):
            for j in range(i + 1, len(route)):
                neighbor = current_route.copy()
                # 交換兩個城市
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                d = calc_total_dist(neighbor)
                
                if d < best_dist:
                    best_dist = d
                    best_neighbor = neighbor
                    
        # 如果沒有更好的鄰居，代表抵達局部最佳解
        if best_neighbor is None:
            break
            
        current_route = best_neighbor
        
    return current_route

print("爬山演算法距離:", calc_total_dist(hill_climbing(initial_route)))

"3."
def simulated_annealing(route, initial_temp=100.0, cooling_rate=0.99):
    current_route = route.copy()
    current_dist = calc_total_dist(current_route)
    best_route, best_dist = current_route.copy(), current_dist
    temp = initial_temp
    
    while temp > 0.1:
        # 隨機挑選兩個城市進行交換
        i, j = random.sample(range(len(route)), 2)
        neighbor = current_route.copy()
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbor_dist = calc_total_dist(neighbor)
        
        # 計算距離差 (能量差)
        delta = neighbor_dist - current_dist
        
        # 如果距離變短，或符合退火機率，則接受新解
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_route = neighbor
            current_dist = neighbor_dist
            
            # 記錄歷史最佳解
            if current_dist < best_dist:
                best_route, best_dist = current_route, current_dist
                
        # 降溫
        temp *= cooling_rate
        
    return best_route

print("模擬退火法距離:", calc_total_dist(simulated_annealing(initial_route)))

"4."
import torch

def gradient_descent_tsp(city_coords, epochs=500, lr=0.05):
    cities_tensor = torch.tensor(city_coords, dtype=torch.float32)
    # 用比城市數量更多的點來模擬一條連續的橡皮筋
    M = len(city_coords) * 3 
    angles = torch.linspace(0, 2 * math.pi, M + 1)[:-1]
    # 初始化一個圓形環
    ring = torch.stack([torch.cos(angles), torch.sin(angles)], dim=1) * 0.5 + 0.5
    ring.requires_grad_(True)
    
    optimizer = torch.optim.Adam([ring], lr=lr)
    
    for epoch in range(epochs):
        optimizer.zero_grad()
        
        # 1. 距離成本：每個城市都要能找到一個夠近的環上節點
        dist_matrix = torch.cdist(cities_tensor, ring)
        min_dists, _ = torch.min(dist_matrix, dim=1)
        loss_data = min_dists.sum()
        
        # 2. 張力成本：環上的節點之間距離越短越好（周長最小化）
        ring_next = torch.roll(ring, shifts=-1, dims=0)
        loss_tension = torch.norm(ring - ring_next, dim=1).sum()
        
        # 總損失 = 靠近城市 + 0.2倍的張力懲罰
        loss = loss_data + 0.2 * loss_tension
        loss.backward()
        optimizer.step()
        
    return ring.detach().numpy()

# 這裡回傳的是連續網格點，後續需要將城市配對到最近的網格點來轉回離散路徑
optimized_ring = gradient_descent_tsp(cities)
print("梯度下降 (彈性網) 節點數量:", len(optimized_ring))

"5."
def greedy_tsp(start_city=0):
    unvisited = list(range(num_cities))
    unvisited.remove(start_city)
    route = [start_city]
    
    while unvisited:
        current = route[-1]
        # 找出未拜訪清單中，距離當前城市最近的目標
        next_city = min(unvisited, key=lambda city: np.linalg.norm(cities[current] - cities[city]))
        route.append(next_city)
        unvisited.remove(next_city)
        
    return route

print("貪婪演算法距離:", calc_total_dist(greedy_tsp(start_city=0)))
