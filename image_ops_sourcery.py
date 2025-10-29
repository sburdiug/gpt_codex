def create_gray_image(width: int, height: int, value: int = 128) -> list[list[int]]:
    """Створює зображення у відтінках сірого як двовимірний список з однаковими значеннями пікселів.

    Функція повертає зображення заданої ширини та висоти, де кожен піксель має однакове значення яскравості.

    Args:
        width (int): Кількість стовпців у зображенні.
        height (int): Кількість рядків у зображенні.
        value (int, optional): Значення яскравості для всіх пікселів. За замовчуванням 128.

    Returns:
        list[list[int]]: Згенероване зображення у відтінках сірого.
    """
    return [[value for _ in range(width)] for _ in range(height)]


def change_brightness(image: list[list[int]], delta: int = 10) -> list[list[int]]:
    """Повертає нове зображення з відкоригованою яскравістю на задану величину.

    Кожен піксель зображення збільшується або зменшується на delta, результат обмежується в межах від 0 до 255.

    Args:
        image (list[list[int]]): Вхідне зображення у відтінках сірого.
        delta (int, optional): Величина зміни яскравості. За замовчуванням 10.

    Returns:
        list[list[int]]: Зображення з відкоригованою яскравістю.
    """
    return [
        [max(0, min(255, pixel + delta)) for pixel in row]
        for row in image
    ]


def blur_image(image: list[list[int]]) -> list[list[int]]:
    """Застосовує простий box blur до зображення у відтінках сірого.

    Кожен піксель у результаті є середнім значенням своїх сусідів у 3x3 області навколо нього.

    Args:
        image (list[list[int]]): Вхідне зображення у відтінках сірого.

    Returns:
        list[list[int]]: Розмите зображення.
    """
    if not image or not image[0]:
        return []

    height = len(image)
    width = len(image[0])
    blurred_image: list[list[int]] = []
    for y in range(height):
        blurred_row: list[int] = []
        for x in range(width):
            neighbors = [
                image[ny][nx]
                for ny in range(max(0, y - 1), min(height, y + 2))
                for nx in range(max(0, x - 1), min(width, x + 2))
            ]
            blurred_row.append(sum(neighbors) // len(neighbors))
        blurred_image.append(blurred_row)
    return blurred_image

if __name__ == "__main__":

    # Arrange
    image = create_gray_image(10, 5, 100)

    # Act
    brighter_image = change_brightness(image, 30)
    blurred_image = blur_image(brighter_image)

    # Assert
    print(blurred_image[0][0])