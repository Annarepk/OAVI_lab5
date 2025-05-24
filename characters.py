from PIL import Image, ImageFont, ImageDraw
import numpy as np

def imgChar(char, fontPath, fontSize, folder):
    font = ImageFont.truetype(fontPath, fontSize)

    tmpImg = Image.new("L", (1, 1), "white")
    tmpDraw = ImageDraw.Draw(tmpImg)
    left, top, right, bottom = tmpDraw.textbbox((0, 0), text=char, font=font)

    charWidth = int(right - left)
    charHeight = int(bottom - top)

    imgWidth = charWidth
    imgHeight = charHeight

    img = Image.new("L", (imgWidth, imgHeight), "white")
    d = ImageDraw.Draw(img)
    d.text((0 - left, 0 - top), char, font=font, fill="black")

    pix = np.array(img)
    coords = np.argwhere(pix < 255)
    if coords.size > 0:
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1
        imgCrop = img.crop((x0, y0, x1, y1))
    else:
        imgCrop = img

    filename = f"{folder}/{char}.bmp"
    imgCrop.save(filename)


def features(filename):
    with Image.open(filename) as img:
        width, height = img.size
        pix = img.load()

        # Вес (масса черного) каждой четверти изображения символа
        weights = [0, 0, 0, 0]  # top-left, top-right, bottom-left, bottom-right
        for x in range(width):
            for y in range(height):
                if pix[x, y] < 128:
                    if x < width // 2 and y < height // 2:
                        weights[0] += 1
                    elif x >= width // 2 and y < height // 2:
                        weights[1] += 1
                    elif x < width // 2 and y >= height // 2:
                        weights[2] += 1
                    else:
                        weights[3] += 1

        # Удельный вес (вес, нормированный к четверти площади)
        areas = [
            (width // 2) * (height // 2),
            (width - width // 2) * (height // 2),
            (width // 2) * (height - height // 2),
            (width - width // 2) * (height - height // 2),
        ]
        normWeights = [weights[i] / areas[i] for i in range(4)]

        # Координаты центра тяжести
        totalWeight = sum(weights)
        if totalWeight == 0:
            centerX = width // 2
            centerY = height // 2
        else:
            sumX, sumY = 0, 0
            for x in range(width):
                for y in range(height):
                    if pix[x, y] < 128:
                        sumX += x
                        sumY += y
            centerX = sumX / totalWeight
            centerY = sumY / totalWeight

        # Нормированные координаты центра тяжести
        normCentX = centerX / width
        normCentY = centerY / height

        # Осевые моменты инерции по горизонтали и вертикали
        inertiaX = 0
        inertiaY = 0
        for x in range(width):
            for y in range(height):
                if pix[x, y] < 128:
                    inertiaX += (y - centerY) ** 2
                    inertiaY += (x - centerX) ** 2

        # Нормированные осевые моменты инерции
        normInertiaX = inertiaX / (width * height)
        normInertiaY = inertiaY / (width * height)

        # Профили X и Y
        profileX = [0] * width
        profileY = [0] * height
        for x in range(width):
            for y in range(height):
                if pix[x, y] < 128:
                    profileX[x] += 1
                    profileY[y] += 1

    return (
        weights,
        normWeights,
        centerX,
        centerY,
        normCentX,
        normCentY,
        inertiaX,
        inertiaY,
        normInertiaX,
        normInertiaY,
        profileX,
        profileY
    )


