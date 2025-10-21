
from typing import List


def make_gray(width: int, height: int, value: int = 128) -> List[List[int]]:
    image = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(value)
        image.append(row)
    return image


def adjust_brightness(image: List[List[int]], delta: int = 10) -> List[List[int]]:
    output = []
    for y in range(len(image)):
        row = []
        for x in range(len(image[0])):
            value = image[y][x] + delta
            if value < 0:
                value = 0
            elif value > 255:
                value = 255
            row.append(value)
        output.append(row)
    return output


def box_blur(image: List[List[int]]) -> List[List[int]]:
    height = len(image)
    width = len(image[0])
    output = []
    for y in range(height):
        row = []
        for x in range(width):
            total = 0
            count = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny = y + dy
                    nx = x + dx
                    if 0 <= ny < height and 0 <= nx < width:
                        total += image[ny][nx]
                        count += 1
            row.append(total // count)
        output.append(row)
    return output


if __name__ == "__main__":
    image = make_gray(10, 5, 100)
    image = adjust_brightness(image, 30)
    image = box_blur(image)
    print(image[0][0])
