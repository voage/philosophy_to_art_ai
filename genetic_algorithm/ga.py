import random


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
    Generates a random artwork representation with stronger philosophical influence.
    """
    stoic_score = ann_scores.get("stoic", 0.5)
    nihilistic_score = ann_scores.get("nihilistic", 0.5)

    # Determine artwork characteristics based on scores
    if nihilistic_score > stoic_score:
        gradient_type = "radial" if random.random() < nihilistic_score else "linear"
        shape_types = (
            ["circle", "rectangle"] if nihilistic_score > 0.7 else ["rectangle"]
        )
        intensity = random.uniform(0.8, 1.0)  # Higher intensity for nihilistic
    else:
        gradient_type = "linear" if random.random() < stoic_score else "radial"
        shape_types = ["circle"] if stoic_score > 0.7 else ["circle", "rectangle"]
        intensity = random.uniform(0.5, 0.8)  # Lower intensity for stoic

    artwork = {
        "color_palette": [
            random_color(stoic_score, nihilistic_score) for _ in range(3)
        ],
        "shapes": [
            {
                "type": random.choice(shape_types),
                "position": (random.randint(0, 300), random.randint(0, 300)),
                "size": random.randint(10, 100),
            }
            for _ in range(random.randint(2, 4))
        ],
        "gradient": {
            "type": gradient_type,
            "direction": random.randint(0, 360),
            "intensity": intensity,
        },
        "philosophical_scores": ann_scores,
    }
    return artwork


POPULATION_SIZE = 100


def initialize_population(size, scores=None):
    """
    Generates initial random population with diverse characteristics
    """
    population = []
    for _ in range(size):
        # Generate completely random artworks
        # Don't bias initial population, let selection pressure guide evolution
        artwork = {
            "color_palette": [
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for _ in range(3)
            ],
            "shapes": [
                {
                    "type": random.choice(["circle", "rectangle"]),
                    "position": (random.randint(0, 300), random.randint(0, 300)),
                    "size": random.randint(10, 100),
                }
                for _ in range(random.randint(2, 4))
            ],
            "gradient": {
                "type": random.choice(["linear", "radial"]),
                "direction": random.randint(0, 360),
                "intensity": random.uniform(0.5, 1.0),
            },
            "philosophical_scores": (
                scores if scores else {"stoic": 0.5, "nihilistic": 0.5}
            ),
        }
        population.append(artwork)
    return population


def fitness_function(individual, ann_output):
    """
    Evaluates the fitness of an individual artwork.
    """
    stoic_score = ann_output["stoic"]
    nihilistic_score = ann_output["nihilistic"]

    # Calculate how well the artwork matches the target emotional balance
    style_match = 0

    # Check gradient type match
    if nihilistic_score > 0.6:  # Strongly nihilistic
        style_match += 1 if individual["gradient"]["type"] == "radial" else 0
    elif stoic_score > 0.6:  # Strongly stoic
        style_match += 1 if individual["gradient"]["type"] == "linear" else 0

    # Color palette evaluation
    color_match = 0
    for color in individual["color_palette"]:
        brightness = sum(color) / (3 * 255)
        saturation = max(color) - min(color)

        if nihilistic_score > stoic_score:
            # Nihilistic prefers darker, more saturated colors
            color_match += (1 - brightness) * 0.7 + (saturation / 255) * 0.3
        else:
            # Stoic prefers balanced, less saturated colors
            color_match += (1 - abs(brightness - 0.6)) * 0.7 + (
                1 - saturation / 255
            ) * 0.3

    color_match /= len(individual["color_palette"])

    # Calculate emotional intensity and match
    target_intensity = abs(
        stoic_score - nihilistic_score
    )  # How extreme the emotion should be
    actual_intensity = abs(color_match - 0.5) * 2  # Convert to 0-1 scale
    intensity_match = 1 - abs(target_intensity - actual_intensity)

    # Weighted combination of all factors
    overall_fitness = style_match * 0.3 + color_match * 0.4 + intensity_match * 0.3

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
        population (list): Initial random population (mix of stoic/nihilistic styles)
        ann_output (dict): Target scores we're evolving towards
        generations (int): Number of generations to evolve
        mutation_rate (float): Chance of mutation
    Returns:
        dict: Best artwork matching target scores
    """
    for generation in range(generations):
        # 1. Evaluate fitness of each individual
        fitness_scores = [
            fitness_function(individual, ann_output) for individual in population
        ]

        # Optional: Print progress
        best_fitness = max(fitness_scores)
        print(f"Generation {generation}: Best Fitness = {best_fitness:.3f}")

        # 2. Select parents for next generation
        next_generation = []
        while len(next_generation) < len(population):
            # Select two parents using roulette wheel selection
            parent1 = roulette_wheel_selection(population, fitness_scores)
            parent2 = roulette_wheel_selection(population, fitness_scores)

            # 3. Perform crossover
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent1, parent2)

            # 4. Perform mutation
            child1 = mutate(child1, mutation_rate, ann_output)
            child2 = mutate(child2, mutation_rate, ann_output)

            next_generation.extend([child1, child2])

        # Replace old population with new generation
        population = next_generation

    # Return the best individual from final generation
    final_fitness_scores = [
        fitness_function(individual, ann_output) for individual in population
    ]
    best_index = final_fitness_scores.index(max(final_fitness_scores))
    return population[best_index]
