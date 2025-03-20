from genetic_algorithm import run_algorithm
import poly_to_raster
import visuals
import config
import utils
import time
from pathlib import Path
from PIL import Image

def plot_results():
    print("Plotting visuals")
    pixel_data = utils.load_pixel_data(image)
    visuals.plot_figure()
    #visuals.plot_grid_lines()
    visuals.plot_grid(pixel_data)
    visuals.plot_steiner_points(result)
    visuals.plot_terminals(terminals)
    visuals.plot_edges(tree)
    #visuals.plot_cell_weights(grid, pixel_data)
    #visuals.plot_edge_weights(tree)
    visuals.display_plot()

def print_results():
    print("-------------Results:-------------")
    print(f"Execution time: {execution_time:.2f} seconds")
    print(f"MST cost: {mst_cost:.4f}")
    print(f"Result fitness: {fitness:.4f}")
    print(f"Improvement over MST: {mst_improvement:.2f}%")

def plot_stats():
    visuals.plot_data_statistics(execution_time, fitness_over_time, "Fitness")


obstacles_path = "problem_instances/slovakia.png"
terminals_path = "problem_instances/slovakia.csv"

ext = Path(obstacles_path).suffix.lower()
if ext == ".csv":
    config.max_cell_weight = poly_to_raster.find_max_weight_in_file(obstacles_path)
    image = poly_to_raster.generate_map_image(obstacles_path, 1000)
elif ext == ".png":
    image = Image.open(obstacles_path).convert('L')
else:
    raise Exception("Wrong obstacle file type! Use .png or .csv")

terminals = utils.read_terminals(terminals_path)
image = image.resize((config.grid_size, config.grid_size), Image.NEAREST)

start_time = time.time()
result, fitness, fitness_over_time = run_algorithm(terminals, image)
end_time = time.time()

execution_time = end_time - start_time
grid = utils.load_grid_weights_from_image(image)
mst_cost = utils.get_fitness(utils.get_weighted_MST(terminals, grid))
tree = utils.get_weighted_MST(terminals + result, grid)
mst_improvement = (abs(fitness - mst_cost) / ((fitness + mst_cost) / 2)) * 100

print_results()
plot_results()
plot_stats()