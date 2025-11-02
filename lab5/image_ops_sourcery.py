def make_gray(width, height, val=128):
    """Створює зображення у відтінках сірого як двовимірний список, де всі пікселі мають однакове значення."""
    return [[val for _ in range(width)] for _ in range(height)]

def adjust_brightness(img, delta=10):
    """Повертає нове зображення з яскравістю, зміненою на delta та обмеженою в межах [0, 255]."""
    return [[max(0, min(255, v + delta)) for v in row] for row in img]

def box_blur(image):
    """Повертає розмиту копію зображення, використовуючи середнє значення у сусідстві 3x3."""
    height, width = len(image), len(image[0])
    return [
        [
            sum(
                image[neighbor_y][neighbor_x]
                for dy in (-1, 0, 1)
                for dx in (-1, 0, 1)
                if 0 <= (neighbor_y := y + dy) < height and 0 <= (neighbor_x := x + dx) < width
            ) // sum(
                1
                for dy in (-1, 0, 1)
                for dx in (-1, 0, 1)
                if 0 <= (y + dy) < height and 0 <= (x + dx) < width
            )
            for x in range(width)
        ]
        for y in range(height)
    ]
if __name__ == "__main__":
    image = make_gray(10, 5, 100)
    image = adjust_brightness(image, 30)
    image = box_blur(image)
    print(image[0][0])