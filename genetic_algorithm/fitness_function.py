def fitness_function(individual, ann_output):
    """
    Evaluates the fitness of an individual artwork.
    """
    stoic_score = ann_output["stoic"]
    nihilistic_score = ann_output["nihilistic"]

    style_match = 0

    if nihilistic_score > 0.6:
        style_match += 1 if individual["gradient"]["type"] == "radial" else 0
    elif stoic_score > 0.6:
        style_match += 1 if individual["gradient"]["type"] == "linear" else 0

    color_match = 0
    for color in individual["color_palette"]:
        brightness = sum(color) / (3 * 255)
        saturation = max(color) - min(color)

        if nihilistic_score > stoic_score:
            color_match += (1 - brightness) * 0.7 + (saturation / 255) * 0.3
        else:
            color_match += (1 - abs(brightness - 0.6)) * 0.7 + (
                1 - saturation / 255
            ) * 0.3

    color_match /= len(individual["color_palette"])

    target_intensity = abs(stoic_score - nihilistic_score)
    actual_intensity = abs(color_match - 0.5) * 2
    intensity_match = 1 - abs(target_intensity - actual_intensity)

    overall_fitness = style_match * 0.3 + color_match * 0.4 + intensity_match * 0.3

    return overall_fitness
