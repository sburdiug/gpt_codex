"""Утилітарні функції для простої обробки зображень у відтінках сірого."""

def _clamp(value: int, *, min_value: int = 0, max_value: int = 255) -> int:
    """Повертає ``value``, обмежене включним діапазоном від ``min_value`` до ``max_value``."""

    return max(min_value, min(value, max_value))


def make_gray(width: int, height: int, value: int = 128) -> list[list[int]]:
    """Створює зображення ``height`` × ``width``, заповнене вказаним сірим значенням ``value``."""

    clamped_value = _clamp(value)
    return [[clamped_value for _ in range(width)] for _ in range(height)]


def adjust_brightness(image: list[list[int]], delta_value: int = 10) -> list[list[int]]:
    """Повертає ``image`` із кожним пікселем, зміненим на ``delta_value`` та обрізаним до діапазону 0–255."""

    return [[_clamp(pixel + delta_value) for pixel in row] for row in image]


def box_blur(image: list[list[int]]) -> list[list[int]]:
    """Повертає розмиту копію ``image``, обчислену як середнє значення в околі 3×3."""

    if not image or not image[0]:
        return []

    height = len(image)
    width = len(image[0])
    blurred: list[list[int]] = []
    for y_coordinate in range(height):
        row: list[int] = []
        for x_coordinate in range(width):
            total = 0
            count = 0
            for neighbor_y in range(max(0, y_coordinate - 1), min(height, y_coordinate + 2)):
                for neighbor_x in range(max(0, x_coordinate - 1), min(width, x_coordinate + 2)):
                    total += image[neighbor_y][neighbor_x]
                    count += 1
            row.append(total // count)
        blurred.append(row)
    return blurred


if __name__ == "__main__":
    image = make_gray(10, 5, 100)
    image = adjust_brightness(image, 30)
    image = box_blur(image)
    print(image[0][0])
