import random


def draw_shape(draw, shape, color_palette, scores):
    """Draws individual shapes with style based on philosophical scores"""
    x, y = shape["position"]
    size = shape["size"]
    color = random.choice(color_palette)

    stoic_score = scores.get("stoic", 0.5)
    nihilistic_score = scores.get("nihilistic", 0.5)

    if shape["type"] == "circle":
        if stoic_score > nihilistic_score:
            draw.ellipse([x, y, x + size, y + size], fill=color)
        else:
            segments = random.randint(3, 8)
            for i in range(segments):
                start_angle = i * (360 / segments)
                end_angle = start_angle + (300 / segments)
                draw.arc(
                    [x, y, x + size, y + size],
                    start_angle,
                    end_angle,
                    fill=color,
                    width=3,
                )

    else:  # rectangle
        if stoic_score > nihilistic_score:
            # Rounded rectangles for stoic
            draw.rounded_rectangle(
                [x, y, x + size, y + size], radius=size // 8, fill=color
            )
        else:
            # Distorted rectangles for nihilistic
            points = [
                (x + random.randint(-10, 10), y + random.randint(-10, 10)),
                (x + size + random.randint(-10, 10), y + random.randint(-10, 10)),
                (
                    x + size + random.randint(-10, 10),
                    y + size + random.randint(-10, 10),
                ),
                (x + random.randint(-10, 10), y + size + random.randint(-10, 10)),
            ]
            draw.polygon(points, fill=color)
