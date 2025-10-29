"""Прості утиліти для роботи з градаціями сірого в Codex CLI."""

from collections.abc import Sequence

Pixel = int
Image = list[list[Pixel]]

__all__ = ("make_gray", "adjust_brightness", "blur", "Brighten", "BLUR")


_MIN_PIXEL = 0
_MAX_PIXEL = 255


def _clamp(value: int, *, lower: int = _MIN_PIXEL, upper: int = _MAX_PIXEL) -> int:
    """Обмежує значення в межах допустимого діапазону градацій сірого."""
    return max(lower, min(value, upper))


def _ensure_rectangular(image: Sequence[Sequence[Pixel]]) -> tuple[int, int]:
    """Перевіряє прямокутність зображення та повертає пару (висота, ширина)."""
    if not image:
        return 0, 0

    width = len(image[0])
    if any(len(row) != width for row in image):
        raise ValueError("All rows in the image must have the same length")
    return len(image), width


def make_gray(width: int, height: int, value: int = 128) -> Image:
    """Повертає зображення у відтінках сірого розміру ``width`` × ``height`` зі значенням ``value``."""
    if width < 0 or height < 0:
        raise ValueError("Image dimensions must be non-negative")

    clamped_value = _clamp(value)
    return [[clamped_value] * width for _ in range(height)]


def adjust_brightness(image: Image, delta: int = 10) -> Image:
    """Повертає копію ``image`` з яскравістю кожного пікселя, зміненою на ``delta``."""
    height, width = _ensure_rectangular(image)
    if not height:
        return []

    return [[_clamp(pixel + delta) for pixel in row] for row in image]


def blur(image: Image) -> Image:
    """Повертає результат розмивання 3×3 для ``image`` з використанням цілочисельного усереднення сусідів."""
    height, width = _ensure_rectangular(image)
    if not height:
        return []

    def blurred_pixel(y: int, x: int) -> int:
        total = 0
        count = 0
        for dy in (-1, 0, 1):
            ny = y + dy
            if 0 <= ny < height:
                for dx in (-1, 0, 1):
                    nx = x + dx
                    if 0 <= nx < width:
                        total += image[ny][nx]
                        count += 1
        return total // count

    return [[blurred_pixel(y, x) for x in range(width)] for y in range(height)]


# Зворотно сумісні псевдоніми для застарілих викликів
Brighten = adjust_brightness
BLUR = blur


if __name__ == "__main__":
    img = make_gray(10, 5, 100)
    img = adjust_brightness(img, 30)
    img = blur(img)
    print(img[0][0])
