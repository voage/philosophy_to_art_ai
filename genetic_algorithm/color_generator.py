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
    if nihilistic_score > stoic_score:
        base_options = [
            (40, 0, 0),  # Dark red
            (20, 20, 20),  # Near black
            (30, 0, 40),  # Dark purple
            (0, 0, 30),  # Dark blue
        ]
        base_color = random.choice(base_options)
        variance = int(20 + (stoic_score * 30))

        return (
            max(0, min(255, base_color[0] + random.randint(-variance, variance))),
            max(0, min(255, base_color[1] + random.randint(-variance, variance))),
            max(0, min(255, base_color[2] + random.randint(-variance, variance))),
        )
    else:
        primary = random.randint(140, 200)
        secondary = random.randint(120, 180)

        color = [secondary, secondary, secondary]
        color[random.randint(0, 2)] = primary

        return tuple(color)
