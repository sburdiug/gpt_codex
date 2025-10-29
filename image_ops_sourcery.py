
def make_gray(width, height, val=128):
    """Creates a grayscale image as a 2D list with all pixels set to a given value.

    This function generates a width x height image where each pixel has the same grayscale value.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.
        val (int, optional): The grayscale value for all pixels. Defaults to 128.

    Returns:
        list[list[int]]: A 2D list representing the grayscale image.
    """
    img = []
    for _ in range(height):
        row = [val for _ in range(width)]
        img.append(row)
    return img

def adjust_brightness(img, delta=10):
    """Adjusts the brightness of a grayscale image by a specified amount.

    This function increases or decreases the brightness of each pixel in the image, clamping values between 0 and 255.

    Args:
        img (list[list[int]]): The input grayscale image as a 2D list.
        delta (int, optional): The amount to adjust brightness by. Defaults to 10.

    Returns:
        list[list[int]]: A new 2D list representing the brightness-adjusted image.
    """
    out = []
    for y in range(len(img)):
        row = []
        for x in range(len(img[0])):
            v = img[y][x] + delta
            v = max(0, min(255, v))
            row.append(v)
        out.append(row)
    return out

def box_blur(img):
    """Applies a box blur filter to a grayscale image.

    This function returns a new image where each pixel is the average of its neighbors in a 3x3 box.

    Args:
        img (list[list[int]]): The input grayscale image as a 2D list.

    Returns:
        list[list[int]]: A new 2D list representing the blurred image.
    """
    h = len(img)
    w = len(img[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            s = 0
            c = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny = y + dy
                    nx = x + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        s += img[ny][nx]
                        c += 1
            row.append(s // c)
        out.append(row)
    return out

if __name__ == "__main__":
    im = make_gray(10, 5, 100)
    im = adjust_brightness(im, 30)
    im = box_blur(im)
    print(im[0][0])

