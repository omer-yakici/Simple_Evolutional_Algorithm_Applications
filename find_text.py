import random
import string
import time

def generate_random_text(length):
    return ''.join(random.choice(string.ascii_letters + string.digits + ' ') for _ in range(length))

def calculate_fitness(target, text):
    return sum(1 for a, b in zip(target, text) if a == b)

def mutate(text, target):
    index = random.randint(0, len(text) - 1)
    mutated = list(text)
    mutated[index] = random.choice(string.ascii_letters + string.digits + ' ')
    mutated = ''.join(mutated)

    if calculate_fitness(target, mutated) > calculate_fitness(target, text):
        return mutated
    else:
        return text

def evolutionary_algorithm(target, population_size=100, generations=1000):
    population = [generate_random_text(len(target)) for _ in range(population_size)]

    for generation in range(generations):
        population.sort(key=lambda x: calculate_fitness(target, x), reverse=True)

        best_fit = population[0]
        print(f"Generation {generation}: {best_fit} (Fitness: {calculate_fitness(target, best_fit)})")
        time.sleep(0.2)

        if best_fit == target:
            print("Target achieved!",str(generation),". is the last generation")
            break

        new_population = [mutate(best_fit, target) for _ in range(population_size - 1)]
        new_population.append(best_fit)
        population = new_population

target_text = "Hello World! I hope you are OK today"

# Run evolutionary algorithm
evolutionary_algorithm(target_text)
