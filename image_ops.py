
from typing import Callable, Iterable, List


Pixel = int
Image = List[List[Pixel]]


def makeGray(width: int, height: int, value: Pixel = 128) -> Image:
    """Повертає двовимірне зображення, заповнене сталим відтінком сірого."""
    if width < 0 or height < 0:
        raise ValueError("width and height must be non-negative")

    return [[value for _ in range(width)] for _ in range(height)]


def _clamp(value: Pixel, *, min_value: Pixel = 0, max_value: Pixel = 255) -> Pixel:
    """Обмежує значення пікселя в межах заданого мінімуму та максимуму."""
    return max(min_value, min(value, max_value))


def _apply_pixelwise(image: Image, transform: Callable[[Pixel], Pixel]) -> Image:
    """Застосовує передану функцію до кожного пікселя зображення."""
    if not image:
        return []

    return [[transform(pixel) for pixel in row] for row in image]


def bright(image: Image, delta: int = 10) -> Image:
    """Повертає копію зображення зі збільшеною яскравістю на вказане значення."""
    return _apply_pixelwise(image, lambda px: _clamp(px + delta))


def Brighten(image: Image, delta: int = 10) -> Image:
    """Сумісний варіант функції bright, який викликає основну реалізацію."""
    return bright(image, delta)


def BLUR(image: Image) -> Image:
    """Повертає розмите зображення шляхом усереднення сусідніх пікселів."""
    if not image:
        return []

    height = len(image)
    width = len(image[0]) if image[0] else 0

    if any(len(row) != width for row in image):
        raise ValueError("Image rows must all have the same length")

    def _neighbors(y: int, x: int) -> Iterable[Pixel]:
        """Повертає значення сусідніх пікселів навколо заданої координати."""
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    yield image[ny][nx]

    def _blur_pixel(y: int, x: int) -> Pixel:
        """Обчислює усереднене значення пікселя для ефекту розмиття."""
        neighbors = tuple(_neighbors(y, x))
        return sum(neighbors) // len(neighbors)

    return [[_blur_pixel(y, x) for x in range(width)] for y in range(height)]

if __name__ == "__main__":
    im = makeGray(10,5,100)
    im = bright(im,30)
    im = BLUR(im)
    print(im[0][0])
