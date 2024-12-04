from .ga_operators import roulette_wheel_selection, crossover, mutate
from .fitness_function import fitness_function

POPULATION_SIZE = 100


def genetic_algorithm(population, ann_output, generations=10, mutation_rate=0.1):
    """
    Runs the Genetic Algorithm to evolve artwork.
    Args:
        population (list): Initial random population (mix of stoic/nihilistic styles)
        ann_output (dict): Target scores we're evolving towards
        generations (int): Number of generations to evolve
        mutation_rate (float): Chance of mutation
    Returns:
        dict: Best artwork matching target scores
    """
    for generation in range(generations):
        fitness_scores = [
            fitness_function(individual, ann_output) for individual in population
        ]

        best_fitness = max(fitness_scores)
        print(f"Generation {generation}: Best Fitness = {best_fitness:.3f}")

        next_generation = []
        while len(next_generation) < len(population):
            parent1 = roulette_wheel_selection(population, fitness_scores)
            parent2 = roulette_wheel_selection(population, fitness_scores)

            child1 = crossover(parent1, parent2)
            child2 = crossover(parent1, parent2)

            child1 = mutate(child1, mutation_rate, ann_output)
            child2 = mutate(child2, mutation_rate, ann_output)

            next_generation.extend([child1, child2])

        population = next_generation

    final_fitness_scores = [
        fitness_function(individual, ann_output) for individual in population
    ]
    best_index = final_fitness_scores.index(max(final_fitness_scores))
    return population[best_index]
