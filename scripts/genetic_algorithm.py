from avoiding_steiner_points import get_avoiding_steiner_points
from delaunay_steiner_points import get_delaunay_steiner_points
import config
import utils as utils
import visuals as visuals
import random
import time
import math

terminals = []
grid = []
avoiding_steiner_points = []

def initialize_population():
    global avoiding_steiner_points
    print("Initializing population")
    population = []
    avoiding_steiner_points_sample = []
    delaunay_steiner_points_sample = []
    avoiding_steiner_points = get_avoiding_steiner_points(terminals, grid)
    delaunay_steiner_points = get_delaunay_steiner_points(terminals)  

    for _ in range(config.population_size):
        if(avoiding_steiner_points):
            random_divider = random.randint(1, math.floor(len(avoiding_steiner_points) / len(terminals)))
            steiner_sample_size = random.randint(0, math.floor(len(avoiding_steiner_points) / random_divider))
            avoiding_steiner_points_sample = random.sample(avoiding_steiner_points, steiner_sample_size)
        if(delaunay_steiner_points):
            delaunay_sample_size = random.randint(0, len(delaunay_steiner_points))
            delaunay_steiner_points_sample = random.sample(delaunay_steiner_points, delaunay_sample_size)
        population.append(avoiding_steiner_points_sample + delaunay_steiner_points_sample)

    print("Optimizing initial generation")
    for i in range(len(population)):
        population[i] = utils.optimize_steiner_points(population[i], terminals, grid)

    print("Population initialization finished")
    return population

def generate_next_generation(population, fitness_values):
    next_generation = []
    for _ in range(len(population) // 2):
        parent1 = tournament_selection(population, fitness_values)
        parent2 = tournament_selection(population, fitness_values)
        child1, child2 = uniform_crossover(parent1, parent2)
        next_generation.extend([child1, child2])
    return next_generation

def tournament_selection(population, fitness_values):
    sample_indices = random.sample(range(len(population)), config.tournament_size)
    best_index = min(sample_indices, key=lambda i: fitness_values[i])
    return population[best_index]

def uniform_crossover(parent1, parent2):
    child1, child2 = [], []
    max_length = max(len(parent1), len(parent2))
    
    for i in range(max_length):
        if i < len(parent1) and i < len(parent2):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        elif i < len(parent1):
            child1.append(parent1[i])
            child2.append(parent1[i])
        elif i < len(parent2):
            child1.append(parent2[i])
            child2.append(parent2[i])
    
    return child1, child2

def mutate_population(population):
    for i in range(len(population)):
        if random.uniform(0, 1) > config.mutation_probability:
            mutation_type_probability = random.uniform(0, 1)
            if mutation_type_probability < 0.5:
                population[i] = move_mutation(population[i], (config.cell_size/2) * (i+1 / len(population)))
            else:
                population[i] = add_mutation(population[i])
    return population

def move_mutation(individual, distance):
    if len(individual) < 1:
        return individual
    for _ in range(random.randint(0, len(individual) - 1)):
        index = random.randint(0, len(individual) - 1)
        modifiers = [-1, 0, 1]
        new_x_pos = distance * random.choice(modifiers)
        new_y_pos = distance * random.choice(modifiers)
        mutated_point = (individual[index][0] + new_x_pos, individual[index][1] + new_y_pos)
        if(utils.is_position_inside_grid(*mutated_point)):
            individual[index] = mutated_point
    return individual

def add_mutation(individual):
    probability = random.uniform(0, 1)
    if probability < 0.5:
        delaunay_steiner_points = get_delaunay_steiner_points(individual + terminals)
        if len(delaunay_steiner_points) > 0: individual.append(random.choice(delaunay_steiner_points))
    else:
        if len(avoiding_steiner_points) > 0: individual.append(random.choice(avoiding_steiner_points))
    return individual

def sort_population_by_fitness(population):
    fitness_population = [(individual, utils.get_fitness(utils.get_weighted_MST(terminals + individual, grid))) for individual in population]
    sorted_population = sorted(fitness_population, key=lambda x: x[1])
    sorted_individuals = [individual for individual, fitness in sorted_population]
    population_fitness = [fitness for individual, fitness in sorted_population]
    return sorted_individuals, population_fitness

def optimization(population):
    print(f"Optimizing individuals in current generation")
    for ii in range(len(population)):
        population[ii] = utils.optimize_steiner_points(population[ii], terminals, grid)

def check_improvements(fitness_values, last_best_fitness, no_improvement_counter):
    terminate = False
    if(fitness_values[0] < last_best_fitness):
        last_best_fitness = fitness_values[0]
        no_improvement_counter = 0
    else:
        no_improvement_counter += 1
        if no_improvement_counter >= config.no_improvement_termination:
            print(f"Result has not improved for {no_improvement_counter} generations.")
            terminate = True
    return last_best_fitness, no_improvement_counter, terminate

def run_algorithm(terminal_points, image):
    print("Starting algorithm")
    global terminals, grid
    terminals = terminal_points
    grid = utils.load_grid_weights_from_image(image)
    no_improvement_counter = 0
    last_best_fitness =  float('inf')
    fitness_over_time = []
    population = initialize_population()
    print(f"Entering algorithm loop for {config.generations} cycles")
    for i in range(config.generations):
        start_time = time.time()
        population, fitness_values = sort_population_by_fitness(population)
        fitness_over_time.append(fitness_values[0])
        best_individual = population[0]
        print(f"Best individual in generation: {fitness_values[0]:.4f}")
        last_best_fitness, no_improvement_counter, terminate = check_improvements(fitness_values, last_best_fitness, no_improvement_counter)
        if terminate: break
        if i > 0: 
            population = generate_next_generation(population, fitness_values)
            population, fitness_values = sort_population_by_fitness(population)
        population = mutate_population(population)
        if(i != 0 and (i % config.optimization_interval == 0 or i == config.generations-1)):
            optimization(population)
        population[config.population_size-1] = best_individual
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Generation {i} - Executed in {execution_time:.2f} seconds")
    
    print("Algorithm done - reached max number of generation")
    print("Returning results")
    sorted_population, population_fitness = sort_population_by_fitness(population)
    result = sorted_population[0]
    fitness = population_fitness[0]
    return result, fitness, fitness_over_time