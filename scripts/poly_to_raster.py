import csv
from PIL import Image, ImageDraw
import config

def read_obstacles(file_path):
    obstacles = []
    weights = []
    current_obstacle = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            row = [item.strip() for item in row if item.strip()]
            
            if len(row) == 1:
                if current_obstacle:
                    obstacles.append(current_obstacle)
                    current_obstacle = []
                weights.append(float(row[0]) if row[0] != "max" else config.max_cell_weight)

            elif len(row) == 2:
                x, y = float(row[0]), float(row[1])
                y = 1 - y
                current_obstacle.append((x, y))

    if current_obstacle:
        obstacles.append(current_obstacle)

    return obstacles, weights

def generate_map_image(file_path, img_size):
    obstacles, weights = read_obstacles(file_path)
    img = Image.new('L', (img_size, img_size), color=255)
    draw = ImageDraw.Draw(img)
    
    for i in range(len(weights)):
        weight = weights[i]
        intensity = int(calculate_pixel_values_from_weights(weight))
        scaled_points = [(int(x * img_size), int(y * img_size)) for x, y in obstacles[i]]
        draw.polygon(scaled_points, fill=intensity)
    
    #img.save("obstacle_map.png")
    return img

def calculate_pixel_values_from_weights(grid):
    normalized_pixel_data = 1 - (grid - config.base_cell_weight) / (config.max_cell_weight - config.base_cell_weight)
    pixel_data = normalized_pixel_data * 255
    return pixel_data

def find_max_weight_in_file(file_path):
    max_weight = float('-inf')
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = [item.strip() for item in row if item.strip()]
            if len(row) == 1:
                weight = float(row[0]) if row[0] != "max" else 1000
                max_weight = max(max_weight, weight)
    
    return max_weight if max_weight != float('-inf') else config.max_cell_weight
