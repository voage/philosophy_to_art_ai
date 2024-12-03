from PIL import Image, ImageDraw
from .gradients import apply_radial_gradient, apply_linear_gradient
from .shapes import draw_shape
from .patterns import add_philosophical_patterns


def visualize_artwork(artwork, filename="best_artwork.png"):
    """
    Visualizes the artwork based on its genotype and saves it as an image.
    Args:
        artwork (dict): The artwork genotype.
        filename (str): The output file name.
    """
    canvas_size = (400, 400)
    image = Image.new("RGB", canvas_size, (255, 255, 255))
    draw = ImageDraw.Draw(image)

    scores = artwork.get("philosophical_scores", {})

    if artwork["gradient"]["type"] == "radial":
        apply_radial_gradient(image, artwork["gradient"], scores)
    else:
        apply_linear_gradient(image, artwork["gradient"], scores)

    add_philosophical_patterns(draw, scores, canvas_size)

    for shape in artwork["shapes"]:
        draw_shape(draw, shape, artwork["color_palette"], scores)

    image.save(filename)
    print(f"Artwork saved as {filename}")


if __name__ == "__main__":
    from ..ga import initialize_population, genetic_algorithm, get_ann_response

    POPULATION_SIZE = 100
    population = initialize_population(POPULATION_SIZE)
    ann_output = get_ann_response()
    best_artwork = genetic_algorithm(population, ann_output, generations=10)

    visualize_artwork(best_artwork, "generated_artwork.png")
