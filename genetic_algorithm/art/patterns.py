import math
import random


def add_philosophical_patterns(draw, scores, canvas_size):
    """Adds background patterns based on philosophical scores"""
    width, height = canvas_size
    stoic_score = scores.get("stoic", 0.5)
    nihilistic_score = scores.get("nihilistic", 0.5)

    if stoic_score > nihilistic_score:
        for i in range(0, width, 40):
            points = []
            for y in range(0, height, 5):
                x = i + math.sin(y / 30) * 20
                points.append((x, y))
            draw.line(points, fill=(255, 255, 255, 100), width=2)
    else:
        for i in range(5):
            points = []
            num_points = random.randint(6, 10)
            center_x = width // 2
            center_y = height // 2
            for j in range(num_points):
                angle = (j / num_points) * 2 * math.pi
                distance = random.randint(100, 200)
                x = center_x + math.cos(angle) * distance
                y = center_y + math.sin(angle) * distance
                points.append((x, y))

            dark_color = (random.randint(0, 30), 0, random.randint(0, 40))
            draw.polygon(points, outline=dark_color, width=2)

            for _ in range(3):
                start_point = random.choice(points)
                end_point = random.choice(points)
                draw.line([start_point, end_point], fill=dark_color, width=2)

        for _ in range(3):
            cx = random.randint(0, width)
            cy = random.randint(0, height)
            spiral_points = []
            for t in range(0, 360, 10):
                r = t / 20
                x = cx + r * math.cos(math.radians(t))
                y = cy + r * math.sin(math.radians(t))
                spiral_points.append((x, y))
            draw.line(spiral_points, fill=(20, 0, 30, 150), width=2)
