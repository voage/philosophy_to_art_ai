from PIL import Image, ImageDraw
import random
import math
from ga import random_color


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

    scores = artwork.get("philosophical_scores", {})

    # Apply background gradient based on philosophical scores
    if artwork["gradient"]["type"] == "radial":
        apply_radial_gradient(image, artwork["gradient"], scores)
    else:  # linear gradient
        apply_linear_gradient(image, artwork["gradient"], scores)

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


# Main Execution

if __name__ == "__main__":
    from ga import initialize_population, genetic_algorithm, get_ann_response

    POPULATION_SIZE = 100
    population = initialize_population(POPULATION_SIZE)
    ann_output = get_ann_response()
    best_artwork = genetic_algorithm(population, ann_output, generations=10)

    visualize_artwork(best_artwork, "generated_artwork.png")
