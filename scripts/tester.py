from genetic_algorithm import run_algorithm
from config import grid_size
from PIL import Image
import poly_to_raster
import time
import utils
import config

def get_additional_run_data(start_time, end_time, fitness):
    execution_time = end_time - start_time
    grid = utils.load_grid_weights_from_image(image)
    mst_cost = utils.get_fitness(utils.get_weighted_MST(terminals, grid))
    mst_improvement = ((mst_cost - fitness) / ((fitness + mst_cost) / 2)) * 100
    return execution_time, mst_cost, mst_improvement


def save_data_to_file(execution_time, mst_cost, fitness, mst_improvement, result, instance_id, run_id):
    file_name = f"{naming}{instance_id}.txt"
    result = [(float(x), float(y)) for x, y in result] # convert np.float64 to python float for print
    
    run_data = (
        f"--------------RUN{run_id}--------------\n"
        f"Execution time: {execution_time:.2f} seconds\n"
        f"MST cost: {mst_cost:.4f}\n"
        f"Result fitness: {fitness:.4f}\n"
        f"Improvement over MST: {mst_improvement:.2f}%\n"
        f"Result: {result}%\n\n"
    )
    
    with open(output+"/"+file_name, "a") as file:
        file.write(run_data)

def calculate_average(instance_id, runs):
    file_name = f"{naming}{instance_id}.txt"
    
    avg_execution_time = total_execution_time / runs
    avg_fitness = total_fitness / runs
    avg_mst_improvement = total_mst_improvement / runs
    
    avg_data = (
        f"--------------AVERAGE--------------\n"
        f"Execution time: {avg_execution_time:.2f} seconds\n"
        f"Result cost: {avg_fitness:.4f}\n"
        f"Improvement over MST: {avg_mst_improvement:.2f}%\n\n"
    )
    
    with open(output+"/"+file_name, "a") as file:
        file.write(avg_data)

def reset_averages():
    global total_execution_time, total_fitness, total_cost, total_fitness_cost_error, total_mst_improvement
    total_execution_time = 0
    total_fitness = 0
    total_cost = 0
    total_fitness_cost_error = 0
    total_mst_improvement = 0

def run_repeatedly(repetitions):
    global total_execution_time, total_fitness, total_cost, total_fitness_cost_error, total_mst_improvement
    for j in range(repetitions):
        print(f"Starting run {j+1} for instance {i}.")
        start_time = time.time()
        result, fitness, fitness_over_time = run_algorithm(terminals, image)
        end_time = time.time()
        execution_time, mst_cost, mst_improvement = get_additional_run_data(start_time, end_time, fitness)
        save_data_to_file(execution_time, mst_cost, fitness, mst_improvement, result, i, j+1)
        total_execution_time += execution_time
        total_fitness += fitness
        total_mst_improvement += mst_improvement

path = "StOBGA_problem_instances/SoftObstacles"
output = "results"
naming = "instance"
instances = [1,2,3,4,5]
runs_per_instance = 10

total_execution_time = 0
total_fitness = 0
total_mst_improvement = 0

for i in instances:
    print(f"Starting runs for instance {i}.")
    reset_averages()
    obstacles_path = path+"/obstacles"+str(i)+".csv"
    terminals_path = path+"/terminals"+str(i)+".csv"
    config.max_cell_weight = poly_to_raster.find_max_weight_in_file(obstacles_path)
    image = poly_to_raster.generate_map_image(obstacles_path, 1000)
    image = image.resize((grid_size, grid_size), Image.NEAREST)
    terminals = utils.read_terminals(terminals_path)
    run_repeatedly(runs_per_instance)
    calculate_average(i, runs_per_instance)