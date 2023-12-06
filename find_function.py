import random
import math
import time

def generate_random_term():
    if random.random() < 0.5:
        return f"{random.uniform(-10, 10)}"
    else:
        return f"{random.choice(['x', 'y'])}"

def generate_individual():
    return f"{generate_random_term()} {random.choice(['+', '-', '*', '**', 'math.sqrt'])} {generate_random_term()} + {random.uniform(-10, 10)}"


def evaluate_function(expr, x, y):
    try:
        result = eval(expr)
        return result
    except:
        # Handle division by zero or other errors
        return float('inf')

def fitness(individual, points):
    error = 0
    for x, y, expected_result in points:
        result = evaluate_function(individual, x, y)
        error += abs(result - expected_result)
    return error

def distance_to_target(individual, points):
    distances = []
    for x, y, expected_result in points:
        result = evaluate_function(individual, x, y)
        distance = abs(result - expected_result)
        distances.append(distance)
    return sum(distances) / len(distances)  # Take mean to return a single value


def crossover(parent1, parent2):
   
    split_point = random.randint(0, min(len(parent1), len(parent2)) - 1)
    child = parent1[:split_point] + parent2[split_point:]
    return child

def mutate(individual, mutation_rate=0.1):
    mutated_individual = list(individual)
    for i in range(len(mutated_individual)):
        if random.random() < mutation_rate:
            mutation_point = random.randint(0, len(mutated_individual) - 1)
            mutated_individual[mutation_point] = generate_individual()
    return ''.join(mutated_individual)

def evolutionary_algorithm(points, population_size=100, generations=1000, crossover_rate=0.8, mutation_rate=0.1, max_stale_generations=3):
    population = [generate_individual() for _ in range(population_size)]
    best_distance = float('inf')
    stale_generations = 0

    for generation in range(generations):
        population = sorted(population, key=lambda x: fitness(x, points))
        best_individual = population[0]

        distance = distance_to_target(best_individual, points)
        print(f"Generation {generation}: Best Function ={best_individual}, Distance = {distance}")
        time.sleep(0.25)

        
        if distance == 0:
            break

        new_population = [best_individual]

        for _ in range(population_size - 1):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])

            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)

            new_population.extend([child])

        population = new_population

        # Reducing existing diversity so that new individuals emerge and diversity increases further
        if generation % 80 == 0:
            population = population[:int(population_size * 0.2)]  # Keep the best %80 

        # If distance does not change, increase stale_generations
        if distance == best_distance:
            stale_generations += 1
        else:
            stale_generations = 0

        # If there are a certain number of consecutive stales (max_stale_generations) or the distance is 0, change the function
        if stale_generations >= max_stale_generations or distance == 0:
            population[1:] = [generate_individual() for _ in range(population_size - 1)]
            stale_generations = 0

        best_distance = distance

    print("\nBest Function Found:", best_individual)
    print("Distance:", distance)

# Given points
points = [(3, 4, 5), (5, 12, 13), (7, 24, 25)]

# Finding the best fitting function using evolutionary algorithm

evolutionary_algorithm(points)
