import config
import numpy as np
import matplotlib.pyplot as plt

def plot_figure():
    plt.figure(figsize=(6, 6))
    plt.xticks(np.arange(0, 1 + config.cell_size, config.cell_size))
    plt.yticks(np.arange(0, 1 + config.cell_size, config.cell_size))
    plt.tick_params(labelsize = 8)
    plt.xticks(rotation = -90)

def plot_grid_lines():
    plt.grid(True, which='both', color='black', linestyle='-', linewidth=0.2)

def plot_grid(pixel_data):
    plt.imshow(pixel_data, cmap='gray', vmin=0, vmax=255, extent=(0, 1, 0, 1), origin='lower')

def plot_terminals(terminals):
    for n in terminals:
        plt.scatter(*n, color='red')

def plot_steiner_points(points):
    for n in points:
        plt.scatter(*n, color='blue')

def plot_edges(tree):
    pos = {}
    for t in tree:
        pos[t] = t

    for e in tree.edges():
        x_values = [pos[e[0]][0], pos[e[1]][0]]
        y_values = [pos[e[0]][1], pos[e[1]][1]]
        plt.plot(x_values, y_values, color="black")

def plot_cell_weights(grid, pixel_data):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            weight = grid[i, j]
            x = j * config.cell_size + config.cell_size / 2
            y = i * config.cell_size + config.cell_size / 2
            pixel_value = pixel_data[i, j] / 255.0
            text_color = 'black' if pixel_value > 0.5 else 'white'
            plt.text(x, y, f"{weight:.2f}", fontsize=5, ha='center', va='center', color=text_color)

def plot_edge_weights(tree):
    pos = {}
    for t in tree:
        pos[t] = t

    for e in tree.edges():
        x_values = [pos[e[0]][0], pos[e[1]][0]]
        y_values = [pos[e[0]][1], pos[e[1]][1]]
        mid_x = (x_values[0] + x_values[1]) / 2
        mid_y = (y_values[0] + y_values[1]) / 2
        edge_weight = tree.get_edge_data(e[0], e[1])['weight']
        edge_weight_str = f"{edge_weight:.2f}"
        plt.text(mid_x, mid_y, edge_weight_str, fontsize=10, ha='center', va='center', color='black')

def display_plot():
    #plt.gca().invert_yaxis()
    plt.show()

def plot_data_statistics(values, title):
    generations = range(1, len(values) + 1)
    plt.figure(figsize=(10, 6))
    plt.plot(generations, values, marker='o', linestyle='-', color='b', label='Values')
    plt.title(title + " over Generations", fontsize=16)
    plt.xlabel("Generations", fontsize=14)
    plt.ylabel(title, fontsize=14)
    plt.xticks(generations)
    plt.show()