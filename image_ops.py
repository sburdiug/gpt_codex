
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


def box_blur(image):
    """Виконує розмиття шляхом усереднення сусідів у вікні 3×3."""
    if not image or not image[0]:
        raise ValueError("Зображення не може бути порожнім для розмиття")

    height = len(image)
    width = len(image[0])
    output = []
    for y in range(height):
        new_row = []
        for x in range(width):
            total = 0
            count = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    new_y = y + dy
                    new_x = x + dx
                    if 0 <= new_y < height and 0 <= new_x < width:
                        total += image[new_y][new_x]
                        count += 1
            new_row.append(total // count)
        output.append(new_row)
    return output


if __name__ == "__main__":
    image = make_gray(10, 5, 100)
    image = adjust_brightness(image, 30)
    image = box_blur(image)
    print(image[0][0])
