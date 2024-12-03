import math


def apply_linear_gradient(image, gradient, scores):
    """
    Applies a linear gradient influenced by philosophical scores.
    """
    width, height = image.size
    stoic_score = scores.get("stoic", 0.5)
    nihilistic_score = scores.get("nihilistic", 0.5)

    pixels = image.load()
    angle = math.radians(gradient["direction"])

    dx = math.cos(angle)
    dy = math.sin(angle)

    for y in range(height):
        for x in range(width):
            pos = (x * dx + y * dy) / (width * abs(dx) + height * abs(dy))
            pos = max(0, min(1, pos))

            if stoic_score > nihilistic_score:
                color = (
                    int(160 + 60 * pos),
                    int(140 + 40 * pos),
                    int(180 + 50 * pos),
                )
            else:
                color = (
                    int(220 - 140 * pos),
                    int(20 + 40 * pos),
                    int(100 + 120 * pos),
                )
            pixels[x, y] = color


def apply_radial_gradient(image, gradient, scores):
    """
    Applies a radial gradient influenced by philosophical scores.
    """
    width, height = image.size
    center_x = width * (0.5 + 0.2 * math.cos(gradient["direction"]))
    center_y = height * (0.5 + 0.2 * math.sin(gradient["direction"]))
    max_radius = math.hypot(
        max(center_x, width - center_x), max(center_y, height - center_y)
    )

    pixels = image.load()
    stoic_score = scores.get("stoic", 0.5)
    nihilistic_score = scores.get("nihilistic", 0.5)
    intensity = gradient["intensity"] * 1.2

    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            distance = math.hypot(dx, dy)
            ratio = (distance / max_radius) * intensity
            ratio = max(0, min(1, ratio))

            if stoic_score > nihilistic_score:
                color = (
                    int(180 - 20 * ratio),  # Subtle red
                    int(160 - 40 * ratio),  # Fading green
                    int(200 - 30 * ratio),  # Strong blue base
                )
            else:
                color = (
                    int(255 - 160 * ratio),  # Strong red fading to purple
                    int(20 + 40 * ratio),  # Low green
                    int(90 + 130 * ratio),  # Increasing blue
                )
            pixels[x, y] = color
