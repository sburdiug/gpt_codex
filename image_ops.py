
def make_gray(width, height, value=128):
    """Створює двовимірний масив з однорідною яскравістю."""
    image = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(value)
        image.append(row)
    return image


def clamp_pixel(value):
    """Обмежує значення пікселя в межах 0-255."""
    return max(0, min(255, value))


def adjust_brightness(image, delta=10):
    """Зміщує яскравість кожного пікселя та обмежує її в діапазоні 0-255."""
    output = []
    for row in image:
        new_row = []
        for pixel in row:
            new_row.append(clamp_pixel(pixel + delta))
        output.append(new_row)
    return output


def blurred_pixel(image, y, x):
    height = len(image)
    width = len(image[0])
    y0, y1 = max(0, y - 1), min(height, y + 2)
    x0, x1 = max(0, x - 1), min(width, x + 2)
    total = sum(
        image[ny][nx]
        for ny in range(y0, y1)
        for nx in range(x0, x1)
    )
    return total // ((y1 - y0) * (x1 - x0))


def box_blur(image):
    """Виконує розмиття шляхом усереднення сусідів у вікні 3×3."""
    if not image or not image[0]:
        raise ValueError("Зображення не може бути порожнім для розмиття")

    height = len(image)
    width = len(image[0])

    return [[blurred_pixel(image, y, x) for x in range(width)] for y in range(height)]


if __name__ == "__main__":
    image = make_gray(10, 5, 100)
    image = adjust_brightness(image, 30)
    image = box_blur(image)
    print(image[0][0])
