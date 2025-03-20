from heapq import heappop, heappush
import utils as utils

def astar(grid, start, goal):
    def get_neighbors(cell):
        row, col = cell
        neighbors = [
            (row - 1, col), (row + 1, col),
            (row, col - 1), (row, col + 1),
            (row - 1, col - 1), (row - 1, col + 1),
            (row + 1, col - 1), (row + 1, col + 1)
        ]
        valid_neighbors = [(r, c) for r, c in neighbors if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]]
        return valid_neighbors


    open_set = []
    heappush(open_set, (0, start))
    came_from = {}

    g_score = {start: 0}
    f_score = {start: utils.euclidean_distance(start, goal)}

    while open_set:
        current_f, current = heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            row, col = neighbor
            if 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]:
                cell_cost = grid[row, col]
                tentative_g_score = g_score[current] + cell_cost
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + utils.euclidean_distance(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], neighbor))

    return None