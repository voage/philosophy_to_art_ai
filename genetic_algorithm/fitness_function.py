def fitness_function(individual, ann_output):
    """
    Evaluates the fitness of an individual artwork.
    """
    stoic_score = ann_output["stoic"]
    nihilistic_score = ann_output["nihilistic"]

    # Calculate how well the artwork matches the target emotional balance
    style_match = 0

    # Check gradient type match
    if nihilistic_score > 0.6:  # Strongly nihilistic
        style_match += 1 if individual["gradient"]["type"] == "radial" else 0
    elif stoic_score > 0.6:  # Strongly stoic
        style_match += 1 if individual["gradient"]["type"] == "linear" else 0

    # Color palette evaluation
    color_match = 0
    for color in individual["color_palette"]:
        brightness = sum(color) / (3 * 255)
        saturation = max(color) - min(color)

        if nihilistic_score > stoic_score:
            # Nihilistic prefers darker, more saturated colors
            color_match += (1 - brightness) * 0.7 + (saturation / 255) * 0.3
        else:
            # Stoic prefers balanced, less saturated colors
            color_match += (1 - abs(brightness - 0.6)) * 0.7 + (
                1 - saturation / 255
            ) * 0.3

    color_match /= len(individual["color_palette"])

    # Calculate emotional intensity and match
    target_intensity = abs(
        stoic_score - nihilistic_score
    )  # How extreme the emotion should be
    actual_intensity = abs(color_match - 0.5) * 2  # Convert to 0-1 scale
    intensity_match = 1 - abs(target_intensity - actual_intensity)

    # Weighted combination of all factors
    overall_fitness = style_match * 0.3 + color_match * 0.4 + intensity_match * 0.3

    return overall_fitness
