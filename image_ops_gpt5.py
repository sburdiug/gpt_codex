"""Прості утиліти роботи з зображеннями у відтінках сірого.

Нотація: пікселі — цілі значення у межах 0..255, зображення —
двовимірний список `list[list[int]]` прямокутної форми.
"""

from collections.abc import Sequence

Pixel = int
Image = list[list[Pixel]]

__all__ = ("make_gray", "adjust_brightness", "blur", "makeGray", "bright", "Brighten", "BLUR")

_MIN = 0
_MAX = 255


def _clamp(v: int, /, *, lo: int = _MIN, hi: int = _MAX) -> int:
    """Обмежує значення пікселя до діапазону [lo, hi]."""
    return max(lo, min(v, hi))


def _ensure_rect(image: Sequence[Sequence[Pixel]]) -> tuple[int, int]:
    """Перевіряє, що зображення прямокутне; повертає (висота, ширина).

    Порожній список вважається коректним з розміром (0, 0).
    """
    if not image:
        return 0, 0
    width = len(image[0])
    if any(len(row) != width for row in image):
        raise ValueError("Усі рядки зображення мають бути однакової довжини")
    return len(image), width


def make_gray(width: int, height: int, value: int = 128) -> Image:
    """Створює зображення розміру ``width``×``height`` зі значенням ``value``.

    - Кидає ValueError, якщо розміри від'ємні.
    - Значення пікселя клампиться до 0..255.
    """
    if width < 0 or height < 0:
        raise ValueError("Розміри зображення мають бути невід'ємними")
    v = _clamp(value)
    return [[v] * width for _ in range(height)]


def adjust_brightness(image: Image, delta: int = 10) -> Image:
    """Повертає копію зображення з доданою яскравістю ``delta`` до кожного пікселя.

    - Порожнє зображення -> порожній результат.
    - Перевіряє прямокутність; при порушенні кидає ValueError.
    - Результат клампиться до 0..255.
    """
    h, w = _ensure_rect(image)
    if h == 0:
        return []
    return [[_clamp(px + delta) for px in row] for row in image]


def blur(image: Image) -> Image:
    """Розмиття (box blur) 3×3 з цілочисельним усередненням сусідів.

    На краях вікно урізається до наявних пікселів; ділення — ціле ``//``.
    """
    h, w = _ensure_rect(image)
    if h == 0:
        return []

    def avg(y: int, x: int) -> int:
        total = 0
        count = 0
        for dy in (-1, 0, 1):
            ny = y + dy
            if 0 <= ny < h:
                for dx in (-1, 0, 1):
                    nx = x + dx
                    if 0 <= nx < w:
                        total += image[ny][nx]
                        count += 1
        return total // count

    return [[avg(y, x) for x in range(w)] for y in range(h)]


# Зворотно сумісні псевдоніми (legacy API)
makeGray = make_gray
bright = adjust_brightness
Brighten = adjust_brightness
BLUR = blur


if __name__ == "__main__":
    # Невелика перевірка роботи функцій
    im = make_gray(10, 5, 100)
    im = adjust_brightness(im, 30)
    im = blur(im)
    print(im[0][0])
