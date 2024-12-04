import random
from .color_generator import random_color


def generate_random_artwork(ann_scores):
    """
    Generates a random artwork representation with stronger philosophical influence.
    """
    stoic_score = ann_scores.get("stoic", 0.5)
    nihilistic_score = ann_scores.get("nihilistic", 0.5)

    if nihilistic_score > stoic_score:
        gradient_type = "radial" if random.random() < nihilistic_score else "linear"
        shape_types = (
            ["circle", "rectangle"] if nihilistic_score > 0.7 else ["rectangle"]
        )
        intensity = random.uniform(0.8, 1.0)
    else:
        gradient_type = "linear" if random.random() < stoic_score else "radial"
        shape_types = ["circle"] if stoic_score > 0.7 else ["circle", "rectangle"]
        intensity = random.uniform(0.5, 0.8)

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


def initialize_population(size, scores=None):
    """
    Generates initial random population with diverse characteristics
    """
    population = []
    for _ in range(size):
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
