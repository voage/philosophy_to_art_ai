import random
from .color_generator import random_color


def roulette_wheel_selection(population, fitness_scores):
    """
    Selects an individual from the population based on fitness-proportionate selection.
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
    """
    child = {
        "color_palette": [
            random.choice([c1, c2])
            for c1, c2 in zip(parent1["color_palette"], parent2["color_palette"])
        ],
        "shapes": random.choice([parent1["shapes"], parent2["shapes"]]),
        "gradient": random.choice([parent1["gradient"], parent2["gradient"]]),
        "philosophical_scores": parent1["philosophical_scores"],
    }
    return child


def mutate(individual, mutation_rate, ann_output):
    """
    Mutates an individual by randomly altering its features.
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
