import random

def make_grid(rows, cols, seed=None):
    if seed is not None:
        random.seed(seed)
    
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    return grid

def place_items(grid, rows, cols, treasure_cnt, trap_cnt):
    placed = 0
    while placed < treasure_cnt + trap_cnt:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)

        if grid[r][c] != '.':
            continue
        
        if placed < treasure_cnt:
            grid[r][c] = 'T'
        else:
            grid[r][c] = 'X'

        placed += 1
    
    return grid

def simulate(grid, rows, cols, start, moves, max_turns=50):
    sr, sc = start 
    hp = 100 
    treasure_count = 0  
    events = [] 
    total_turns = 0  
    total_treasures = sum(row.count('T') for row in grid) 
    
    while total_turns < max_turns:
        if treasure_count == total_treasures:
            events.append("early_clear")
            break
        
        if hp <= 0:
            events.append("hp_zero")
            break
        
        if total_turns < len(moves):  
            move = moves[total_turns]  
        else:
            break  

        total_turns += 1
        
        if move == 'U': sr -= 1
        elif move == 'D': sr += 1
        elif move == 'L': sc -= 1
        elif move == 'R': sc += 1
        
        if sr < 0 or sr >= rows or sc < 0 or sc >= cols:
            sr, sc = start  
            continue
        
        current_pos = grid[sr][sc]
        
        if current_pos == 'T':
            treasure_count += 1
            grid[sr][sc] = '.' 
            events.append(f"treasure")
        
        elif current_pos == 'X':
            hp -= 15  
            events.append(f"trap")
        
        print(f"Turn {total_turns}: ({sr},{sc}) {current_pos}")
    
    stats = [sr, sc, total_turns, hp, treasure_count, total_treasures - treasure_count]
    return events, stats, grid

def score_run(base, *events, bonus_rate=1.0, treasure_delta=12, trap_delta=-8, early_clear_delta=25):
    score = base
    for event in events:
        if event == "treasure":
            score += treasure_delta
        elif event == "trap":
            score += trap_delta
        elif event == "early_clear":
            score += early_clear_delta
    
    score = int(score * bonus_rate)
    return score

if __name__ == "__main__":
    rows, cols = map(int, input("Rows and Cols 입력: ").split())
    seed = input("Seed 입력 (없으면 Enter): ")
    seed = int(seed) if seed else None
    treasure_cnt, trap_cnt = map(int, input("Treasure Count, Trap Count 입력: ").split())
    sr, sc = map(int, input("Start 위치 (sr sc) 입력: ").split())
    moves = input("이동 명령 입력 (예: RRDDLU...): ").strip()

    valid_moves = {'U', 'D', 'L', 'R'}
    if any(move not in valid_moves for move in moves):
        print("잘못된 이동 명령이 포함되어 있습니다. 'U', 'D', 'L', 'R'만 사용할 수 있습니다.")
        exit()  

    grid = make_grid(rows, cols, seed)

    grid = place_items(grid, rows, cols, treasure_cnt, trap_cnt)

    events, stats, updated_grid = simulate(grid, rows, cols, [sr, sc], moves)

    print("\n=== 탐험 결과 ===")
    print(f"최종 위치: ({stats[0]},{stats[1]})")
    print(f"턴 수: {stats[2]}")
    print(f"HP: {stats[3]}")
    print(f"회수한 보물: {stats[4]}")
    print(f"남은 보물(재검산): {stats[5]}")
    score = score_run(100, *events)
    print(f"최종 점수: {score}")