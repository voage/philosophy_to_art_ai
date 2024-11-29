import random


def get_ann_response():
    """
    Simulates the ANN output for a philosophical text.
    Returns a dictionary with emotion scores.
    """
    return {
        "stoic": 0.1,
        "nihilistic": 0.9,
    }


def random_color(stoic_score, nihilistic_score):
    """
    Generates a color based on both stoic and nihilistic scores.
    Stoic: Influences how muted/calm the colors are
    Nihilistic: Influences contrast and darkness

    Args:
        stoic_score (float): 0-1 score for stoicism
        nihilistic_score (float): 0-1 score for nihilism
    """
    # Base color options for different philosophical combinations
    if stoic_score > nihilistic_score:
        base_options = [
            (200, 190, 180),  # Beige
            (180, 180, 180),  # Gray
            (170, 190, 200),  # Soft blue
            (190, 180, 170),  # Warm gray
        ]
        base_color = random.choice(base_options)
        variance = int(20 + (nihilistic_score * 30))

        return (
            max(0, min(255, base_color[0] + random.randint(-variance, variance))),
            max(0, min(255, base_color[1] + random.randint(-variance, variance))),
            max(0, min(255, base_color[2] + random.randint(-variance, variance))),
        )
    else:
        primary = random.randint(180 - int(stoic_score * 80), 255)
        secondary = random.randint(0, 50 + int(stoic_score * 50))

        color = [secondary, secondary, secondary]
        color[random.randint(0, 2)] = primary

        return tuple(color)


def generate_random_artwork(ann_scores):
    """
    Generates a random artwork representation.
    Args:
        ann_scores (dict): Dictionary containing both stoic and nihilistic scores
    """
    stoic_score = ann_scores["stoic"]
    nihilistic_score = ann_scores["nihilistic"]

    artwork = {
        "color_palette": [
            random_color(stoic_score, nihilistic_score) for _ in range(3)
        ],
        "shapes": [
            {
                "type": random.choice(["circle", "rectangle"]),
                "position": (
                    random.randint(0, 300),
                    random.randint(0, 300),
                ),
                "size": random.randint(10, 100),
            }
            for _ in range(2)
        ],
        "gradient": {
            "type": random.choice(["linear", "radial"]),
            "direction": random.randint(0, 360),
            "intensity": random.uniform(0.5, 1.0),
        },
        "philosophical_scores": ann_scores,  # Include the scores in the artwork
    }
    return artwork


POPULATION_SIZE = 100


def initialize_population(size):
    """
    Generates an initial population of artworks.
    Args:
        size (int): The number of individuals in the population.
    Returns:
        list: A list of artwork genotypes.
    """
    ann_output = get_ann_response()
    population = []

    for _ in range(size):
        artwork = generate_random_artwork(ann_output)
        population.append(artwork)

    return population


def fitness_function(individual, ann_output):
    """
    Evaluates the fitness of an individual artwork.
    Args:
        individual (dict): The artwork genotype.
        ann_output (dict): The ANN emotional scores.
    Returns:
        float: The fitness score (higher is better).
    """
    stoic_score = ann_output["stoic"]
    nihilistic_score = ann_output["nihilistic"]

    color_fitness = 0
    for color in individual["color_palette"]:
        brightness = sum(color) / (3 * 255)  # Normalize brightness to 0-1
        if stoic_score > nihilistic_score:
            color_fitness += brightness  # Favor brighter colors
        else:
            color_fitness += 1 - brightness  # Favor darker colors

    color_fitness /= len(individual["color_palette"])

    # Adjust overall fitness based on dominant emotion
    dominant_emotion_score = max(stoic_score, nihilistic_score)
    overall_fitness = color_fitness * 0.7 + dominant_emotion_score * 0.3

    return overall_fitness


def roulette_wheel_selection(population, fitness_scores):
    """
    Selects an individual from the population based on fitness-proportionate selection.
    Args:
        population (list): The current population of individuals.
        fitness_scores (list): The fitness scores of the individuals.
    Returns:
        dict: The selected individual.
    """
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    selected_index = random.choices(range(len(population)), weights=probabilities, k=1)[
        0
    ]
    return population[selected_index]


def crossover(parent1, parent2):
    """
    Performs crossover between two parents to produce a child.
    Args:
        parent1 (dict): The first parent genotype.
        parent2 (dict): The second parent genotype.
    Returns:
        dict: The child genotype.
    """
    child = {
        "color_palette": [
            random.choice([c1, c2])
            for c1, c2 in zip(parent1["color_palette"], parent2["color_palette"])
        ],
        "shapes": random.choice([parent1["shapes"], parent2["shapes"]]),
        "gradient": random.choice([parent1["gradient"], parent2["gradient"]]),
        "philosophical_scores": parent1["philosophical_scores"],  # Inherit from parent
    }
    return child


def mutate(individual, mutation_rate, ann_output):
    """
    Mutates an individual by randomly altering its features.
    Args:
        individual (dict): The individual genotype.
        mutation_rate (float): The probability of mutation.
        ann_output (dict): Dictionary containing philosophical scores.
    Returns:
        dict: The mutated individual.
    """
    if random.random() < mutation_rate:
        individual["color_palette"] = [
            random_color(ann_output["stoic"], ann_output["nihilistic"])
            for _ in range(3)
        ]

    if random.random() < mutation_rate:
        individual["shapes"] = [
            {
                "type": random.choice(["circle", "rectangle"]),
                "position": (random.randint(0, 300), random.randint(0, 300)),
                "size": random.randint(10, 100),
            }
            for _ in range(2)
        ]

    if random.random() < mutation_rate:
        individual["gradient"] = {
            "type": random.choice(["linear", "radial"]),
            "direction": random.randint(0, 360),
            "intensity": random.uniform(0.5, 1.0),
        }

    return individual


def genetic_algorithm(population, ann_output, generations=10, mutation_rate=0.1):
    """
    Runs the Genetic Algorithm to evolve artwork.
    Args:
        population (list): The initial population of individuals.
        ann_output (dict): The target emotional scores from the ANN.
        generations (int): The number of generations to run.
        mutation_rate (float): The probability of mutation.
    Returns:
        dict: The best individual from the final generation.
    """
    for _ in range(generations):
        fitness_scores = []

        for individual in population:
            score = fitness_function(individual, ann_output)
            fitness_scores.append(score)

        next_generation = []

        for _ in range(len(population) // 2):
            parent1 = roulette_wheel_selection(population, fitness_scores)
            parent2 = roulette_wheel_selection(population, fitness_scores)

            child1 = crossover(parent1, parent2)
            child2 = crossover(parent1, parent2)

            child1 = mutate(child1, mutation_rate, ann_output)
            child2 = mutate(child2, mutation_rate, ann_output)

            next_generation.extend([child1, child2])

        population = next_generation

    final_fitness_scores = []

    for individual in population:
        score = fitness_function(individual, ann_output)
        final_fitness_scores.append(score)

    best_index = final_fitness_scores.index(max(final_fitness_scores))
    return population[best_index]
