import config
import numpy as np
import networkx as nx
from scipy.spatial import distance
import math
import csv

def load_grid_weights_from_image(img):
    grid = np.ones((config.grid_size, config.grid_size))
    pixel_data = load_pixel_data(img)
    normalized_pixel_data = pixel_data / 255.0
    grid = config.base_cell_weight + (config.max_cell_weight - config.base_cell_weight) * (1 - normalized_pixel_data)
    return grid

def load_pixel_data(img):
    pixel_data = np.array(img)
    pixel_data = pixel_data[::-1] # flip y axis
    return pixel_data

def read_terminals(file_path):
    terminals = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            x, y = map(float, row)
            terminals.append((x, y))
    
    return terminals

def grid_to_position(row, column):
    x = column * config.cell_size + config.cell_size / 2
    y = row * config.cell_size + config.cell_size / 2
    return x, y

def position_to_grid(x, y):
    row = int(y // config.cell_size)
    column = int(x // config.cell_size)
    return row, column

def is_position_inside_grid(x, y):
    max_x = config.grid_size * config.cell_size
    max_y = config.grid_size * config.cell_size

    return 0 <= x < max_x and 0 <= y < max_y

def euclidean_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def get_coordinate_on_line(point1, point2, x=None, y=None):
    x1, y1 = point1
    x2, y2 = point2
    
    if x1 == x2:
        if y is not None:
            if min(y1, y2) <= y <= max(y1, y2):
                return (x1, y)
    
    elif y1 == y2:
        if x is not None:
            if min(x1, x2) <= x <= max(x1, x2):
                return (x, y1)
    else:
        if x is not None:
            y = y1 + (y2 - y1) * (x - x1) / (x2 - x1)
            if min(x1, x2) <= x <= max(x1, x2):
                return (x, y)
        elif y is not None:
            x = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
            if min(y1, y2) <= y <= max(y1, y2):
                return (x, y)

    return None

def clamp(n, min_value, max_value):
    return max(min_value, min(n, max_value))

def get_cells_on_line(point1, point2): # Implementation of Amanatides and Woo's algorithm
    cells = []
    x1, y1 = position_to_grid(*point1)
    x2, y2 = position_to_grid(*point2)
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1
    
    t_max_x = (config.cell_size - (point1[0] % config.cell_size)) / (dx + 1e-6)
    t_max_y = (config.cell_size - (point1[1] % config.cell_size)) / (dy + 1e-6)
    
    t_delta_x = config.cell_size / dx if dx != 0 else float('inf')
    t_delta_y = config.cell_size / dy if dy != 0 else float('inf')
    
    x, y = x1, y1
    epsilon = 1
    max_iterations = 10000
    iteration_count = 0
    
    while iteration_count < max_iterations:
        cells.append((x, y))

        if abs(x - x2) < epsilon and abs(y - y2) < epsilon:
            break
        
        if t_max_x < t_max_y:
            t_max_x += t_delta_x
            x += sx
        else:
            t_max_y += t_delta_y
            y += sy
        
        iteration_count += 1
        if iteration_count >= max_iterations:
            break

    cells.append((x2, y2))
    return cells

def get_fitness(mst):
    total_weight = sum(edge[2]['weight'] for edge in mst.edges(data=True))
    return total_weight

def get_weighted_MST(points, grid):
    G = nx.Graph()

    for i in range(len(points)):
        for j in range(i+1, len(points)):
            weight = get_edge_weight(points[i], points[j], grid)
            G.add_edge(points[i], points[j], weight=weight)

    return nx.minimum_spanning_tree(G)

def get_edge_weight(point1, point2, grid):
    min_x = min(point1[0], point2[0])
    max_x = max(point1[0], point2[0])
    min_y = min(point1[1], point2[1])
    max_y = max(point1[1], point2[1])

    vertical_intersections = [get_coordinate_on_line(point1, point2, x=(i * config.cell_size)) 
                              for i in range(1, config.grid_size) if min_x <= i * config.cell_size <= max_x]
    horizontal_intersections = [get_coordinate_on_line(point1, point2, y=(i * config.cell_size)) 
                                for i in range(1, config.grid_size) if min_y <= i * config.cell_size <= max_y]
    
    line_grid_intersections = [p for p in vertical_intersections + horizontal_intersections if p is not None]
    line_grid_intersections.sort(key=lambda p: euclidean_distance(point1, p))

    total_weight = 0
    current_point = point1
    
    for next_point in line_grid_intersections + [point2]:
        weight = euclidean_distance(current_point, next_point)

        mid_x, mid_y = (current_point[0] + next_point[0]) / 2, (current_point[1] + next_point[1]) / 2
        row, col = position_to_grid(mid_x, mid_y)

        cell_weight = grid[row, col]
        weighted_segment = weight * cell_weight
        total_weight += weighted_segment

        current_point = next_point
    
    return total_weight

def angle_between_edges(p1, p2, p3):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    
    u = p1 - p2
    v = p3 - p2
    
    cos_theta = 1 - distance.cosine(u, v)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angle_radians = np.arccos(cos_theta)
    angle_degrees = np.degrees(angle_radians)
    
    return angle_degrees

def are_points_equal(p1, p2, tolerance=1e-6):
    return abs(p1[0] - p2[0]) < tolerance and abs(p1[1] - p2[1]) < tolerance

def optimize_steiner_points(individual, terminals, grid):
    tree = get_weighted_MST(terminals + individual, grid)

    for point in individual:
        if point not in tree.nodes:
            continue

        neighbors = list(tree.neighbors(point))

        if len(neighbors) > 2:
            continue

        if len(neighbors) == 1:
            tree.remove_node(point)
            continue

        if any(are_points_equal(point, terminal) for terminal in terminals):
            tree.remove_node(point)
            new_cost = (get_edge_weight(neighbors[0], neighbors[1], grid))
            tree.add_edge(neighbors[0], neighbors[1], weight=new_cost)
            continue

        angle = angle_between_edges(neighbors[0], point, neighbors[1])
        if angle > 179:
            tree.remove_node(point)
            new_cost = (get_edge_weight(neighbors[0], neighbors[1], grid))
            tree.add_edge(neighbors[0], neighbors[1], weight=new_cost)
            continue

        current_cost = (get_edge_weight(neighbors[0], point, grid) + get_edge_weight(point, neighbors[1], grid))
        new_cost = (get_edge_weight(neighbors[0], neighbors[1], grid))
        if new_cost <= current_cost:
            tree.remove_node(point)
            tree.add_edge(neighbors[0], neighbors[1], weight=new_cost)
            continue
    
    return list(set(tree.nodes()) - set(terminals))