import config
import utils as utils
import astar as astar

def find_avoiding_steiner_points(terminals, grid):
    print("Looking for avoiding Steiner points")
    avoiding_steiner_points = []
    checked = []
    for terminal in terminals:
        if (terminal not in checked):
            starting_terminal = terminal
            checked.append(starting_terminal)
            closest = starting_terminal
            shortest = float('inf')
            for terminal in terminals:
                if (terminal not in checked):
                    dist = utils.euclidean_distance(starting_terminal, terminal)
                    if (dist < shortest):
                        closest = terminal
            line_coordinates = utils.get_cells_on_line(starting_terminal, closest)
            for coord in line_coordinates:
                if grid[coord[0]][coord[1]] > config.base_cell_weight:
                    start = utils.position_to_grid(*starting_terminal)
                    goal = utils.position_to_grid(*closest)
                    path = astar.astar(grid, start, goal)
                    avoiding_steiner_points += add_steiner_points_on_path(path)
                    break

    print(f"Found {len(avoiding_steiner_points)} avoiding Steiner points")
    print("Removing duplicate avoiding Steiner points")
    filtered_avoiding_steiner_points = []
    for item in avoiding_steiner_points:
        if not any(utils.are_points_equal(item, terminal) for terminal in terminals) and item not in filtered_avoiding_steiner_points:
            filtered_avoiding_steiner_points.append(item)

    print(f"Avoiding Steiner points without duplicates: {len(filtered_avoiding_steiner_points)}")
    return filtered_avoiding_steiner_points

def add_steiner_points_on_path(path):
    steiner_points = []
    
    if path != None:
        for i in range(1, len(path)-1):
            steiner_points.append(utils.grid_to_position(*path[i]))

    return steiner_points

def add_corner_steiner_points(steiner_points):
    corner_points = []
    half_cell = (config.cell_size / 2) - 0.001

    for point in steiner_points:
        corner_points.append((point[0] - half_cell, point[1] - half_cell))
        corner_points.append((point[0] + half_cell, point[1] - half_cell))
        corner_points.append((point[0] - half_cell, point[1] + half_cell))
        corner_points.append((point[0] + half_cell, point[1] + half_cell))

    return steiner_points + corner_points

def get_avoiding_steiner_points(terminals, grid):
    avoiding_steiner_points = find_avoiding_steiner_points(terminals, grid)
    if(len(avoiding_steiner_points) <= 0):
        print("No avoiding Steiner point needed")
        return avoiding_steiner_points
    avoiding_steiner_points = utils.optimize_steiner_points(avoiding_steiner_points, terminals, grid)
    avoiding_steiner_points = add_corner_steiner_points(avoiding_steiner_points)
    print("Avoiding Steiner point generation finished")
    return avoiding_steiner_points