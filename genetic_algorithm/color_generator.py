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
