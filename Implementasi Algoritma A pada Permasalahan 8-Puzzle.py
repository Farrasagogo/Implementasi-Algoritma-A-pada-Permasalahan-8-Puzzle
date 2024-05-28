from heapq import heappop, heappush

class PuzzleState:
    def __init__(self, board, empty_pos, g=0, h=0, parent=None):
        self.board = board
        self.empty_pos = empty_pos
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):
        return self.f < other.f

def manhattan_heuristic(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != 0:
                x, y = divmod(state.board[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance

def misplaced_tiles_heuristic(state, goal):
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != 0 and state.board[i][j] != goal.board[i][j]:
                misplaced += 1
    return misplaced

def astar_solver(start, goal):
    open_list = []
    closed_set = set()
    heappush(open_list, start)

    while open_list:
        current_state = heappop(open_list)
        closed_set.add(tuple(map(tuple, current_state.board)))

        if current_state.board == goal.board:
            return reconstruct_path(current_state)

        neighbors = generate_neighbors(current_state)

        for neighbor in neighbors:
            if tuple(map(tuple, neighbor.board)) in closed_set:
                continue

            neighbor.g = current_state.g + 1
            neighbor.h = manhattan_heuristic(neighbor, goal)
            neighbor.f = neighbor.g + neighbor.h
            heappush(open_list, neighbor)

    return None

def reconstruct_path(state):
    path = []
    while state:
        path.append(state.board)
        state = state.parent
    return path[::-1]

def generate_neighbors(state):
    neighbors = []
    x, y = state.empty_pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_board = [row[:] for row in state.board]
            new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
            neighbors.append(PuzzleState(new_board, (nx, ny), parent=state))

    return neighbors

def is_solvable(board):
    flat_board = [num for row in board for num in row if num != 0]
    inversion_count = sum(flat_board[i] > flat_board[j] for i in range(len(flat_board)) for j in range(i + 1, len(flat_board)))
    return inversion_count % 2 == 0

def main():
    start_board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]

    goal_board = [
        [1, 2, 3],
        [0, 4, 5],
        [6, 7, 8]
    ]

    if not is_solvable(start_board):
        print("The puzzle is not solvable.")
        return

    start_state = PuzzleState(start_board, (2, 1))
    goal_state = PuzzleState(goal_board, (2, 2))

    solution = astar_solver(start_state, goal_state)

    if solution:
        for step in solution:
            for row in step:
                print(row)
            print()
    else:
        print("No solution found")

if __name__ == "__main__":
    main()