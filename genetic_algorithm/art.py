from PIL import Image, ImageDraw
import random
import math
from .ga import random_color


def visualize_artwork(artwork, filename="best_artwork.png"):
    """
    Visualizes the artwork based on its genotype and saves it as an image.
    Args:
        artwork (dict): The artwork genotype.
        filename (str): The output file name.
    """
    # Create a blank canvas
    canvas_size = (400, 400)
    image = Image.new("RGB", canvas_size, (255, 255, 255))
    draw = ImageDraw.Draw(image)

    scores = artwork.get("philosophical_scores", {})

    # Apply background gradient
    if artwork["gradient"]["type"] == "radial":
        apply_radial_gradient(image, artwork["gradient"], scores)
    else:
        apply_linear_gradient(image, artwork["gradient"], scores)

    # Add philosophical patterns
    add_philosophical_patterns(draw, scores, canvas_size)

    # Draw shapes from the artwork genotype
    for shape in artwork["shapes"]:
        draw_shape(draw, shape, artwork["color_palette"], scores)

    # Save the image
    image.save(filename)
    print(f"Artwork saved as {filename}")


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
    intensity = (
        gradient["intensity"] * 1.2
    )  # Increased intensity for more dramatic effect

    for y in range(height):
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            distance = math.hypot(dx, dy)
            ratio = (distance / max_radius) * intensity
            ratio = max(0, min(1, ratio))

            if stoic_score > nihilistic_score:
                # Stoic: Peaceful lavender gradients
                color = (
                    int(180 - 20 * ratio),  # Subtle red
                    int(160 - 40 * ratio),  # Fading green
                    int(200 - 30 * ratio),  # Strong blue base
                )
            else:
                # Nihilistic: Bold red to purple gradients
                color = (
                    int(255 - 160 * ratio),  # Strong red fading to purple
                    int(20 + 40 * ratio),  # Low green for richness
                    int(90 + 130 * ratio),  # Increasing blue for purple
                )
            pixels[x, y] = color


def draw_shape(draw, shape, color_palette, scores):
    """Draws individual shapes with style based on philosophical scores"""
    x, y = shape["position"]
    size = shape["size"]
    color = random.choice(color_palette)

    stoic_score = scores.get("stoic", 0.5)
    nihilistic_score = scores.get("nihilistic", 0.5)

    if shape["type"] == "circle":
        if stoic_score > nihilistic_score:
            # Smooth, complete circles for stoic
            draw.ellipse([x, y, x + size, y + size], fill=color)
        else:
            # Fragmented circles for nihilistic
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


def add_philosophical_patterns(draw, scores, canvas_size):
    """Adds background patterns based on philosophical scores"""
    width, height = canvas_size
    stoic_score = scores.get("stoic", 0.5)
    nihilistic_score = scores.get("nihilistic", 0.5)

    if stoic_score > nihilistic_score:
        # Keep the existing flowing, harmonious curves for stoic
        for i in range(0, width, 40):
            points = []
            for y in range(0, height, 5):
                x = i + math.sin(y / 30) * 20
                points.append((x, y))
            draw.line(points, fill=(255, 255, 255, 100), width=2)
    else:
        # Create more sophisticated nihilistic patterns
        # Geometric fractured pattern
        for i in range(5):  # Create several layers
            # Create a large polygon with jagged edges
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

            # Draw with semi-transparent dark colors
            dark_color = (random.randint(0, 30), 0, random.randint(0, 40))
            draw.polygon(points, outline=dark_color, width=2)

            # Add intersecting lines within the polygon
            for _ in range(3):
                start_point = random.choice(points)
                end_point = random.choice(points)
                draw.line([start_point, end_point], fill=dark_color, width=2)

        # Add some spiral elements
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


# Main Execution

if __name__ == "__main__":
    from ga import initialize_population, genetic_algorithm, get_ann_response

    POPULATION_SIZE = 100
    population = initialize_population(POPULATION_SIZE)
    ann_output = get_ann_response()
    best_artwork = genetic_algorithm(population, ann_output, generations=10)

    visualize_artwork(best_artwork, "generated_artwork.png")
