import random
import math

def generate_random_term():
    return f"{random.choice(['x', 'y'])} ** {random.uniform(1, 3)}"

def generate_random_function():
    term1 = generate_random_term()
    operator = random.choice(['+', '-', '*', '**', 'math.sqrt'])
    term2 = generate_random_term()
    constant = random.uniform(-10, 10)
    return f"({term1}) {operator} ({term2}) + {constant}"

def evaluate_function(expr, x, y):
    try:
        result = eval(expr)
        return result
    except:
        # Handle division by zero or other errors
        return float('inf')

def fitness(individual, points):
    errors = []
    for x, y, expected_result in points:
        result = evaluate_function(individual, x, y)
        error = abs(result - expected_result)
        errors.append(error)
    return errors

def crossover(parent1, parent2):
    split_point = random.randint(0, min(len(parent1), len(parent2)) - 1)
    child = parent1[:split_point] + parent2[split_point:]
    return child

def mutate(individual, mutation_rate=0.1):
    mutated_individual = list(individual)
    for i in range(len(mutated_individual)):
        if random.random() < mutation_rate:
            mutation_point = random.randint(0, len(mutated_individual) - 1)
            mutated_individual[mutation_point] = generate_random_term()
    return ''.join(mutated_individual)

def evolutionary_algorithm(points, population_size=50, generations=10000, crossover_rate=0.8, mutation_rate=0.1, max_stale_generations=3, convergence_threshold=0.01, max_same_function_generations=5):
    population = [generate_random_function() for _ in range(population_size)]
    stale_generations = 0
    same_function_generations = 0
    best_distance = float('inf')  

    for generation in range(generations):
        population = sorted(population, key=lambda x: sum(fitness(x, points)))
        best_individual = population[0]

        distances = fitness(best_individual, points)
        total_distance = sum(distances)

        print(f"Generation {generation}: Best Function = {best_individual}, Distances = {distances}, Total Distance = {total_distance}")

        if total_distance <= convergence_threshold:
            print("Optimization successful. Target reached.")
            break

        new_population = [best_individual]

        if same_function_generations >= max_same_function_generations:
            population[1:] = [generate_random_function() for _ in range(population_size - 1)]
            same_function_generations = 0
        else:
            same_function_generations += 1

        for _ in range(population_size - 1):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])

            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)

            new_population.extend([child])

        population = new_population

        if total_distance == best_distance:
            stale_generations += 1
        else:
            stale_generations = 0

        if stale_generations >= max_stale_generations:
            population[1:] = [generate_random_function() for _ in range(population_size - 1)]
            stale_generations = 0

        best_distance = total_distance

    print("\nBest Function Found:", best_individual)
    print("Distances:", distances)
    print("Total Distance:", total_distance)

points = [(3, 4, 5), (5, 12, 13), (7, 24, 25)]

evolutionary_algorithm(points)
