import csv
import matplotlib.pyplot as plt
from characters import imgChar, features

fontPath = "times_new_roman.ttf"
fontSize = 52
alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"
folderLet = "letters"
folderProf = "profiles"
data = []

for char in alphabet:
    imgChar(char, fontPath, fontSize, folderLet)
    print(f"The character '{char}' is saved in the folder {folderLet}...")
    filename = f"{folderLet}/{char}.bmp"
    (
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
    ) = features(filename)

    data.append(
        [
            char,
            weights,
            normWeights,
            centerX,
            centerY,
            normCentX,
            normCentY,
            inertiaX,
            inertiaY,
            normInertiaX,
            normInertiaY
        ]
    )

    # Сохранение профилей X и Y в виде графиков
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.barh(range(len(profileX)), profileX)
    plt.ylabel("X")
    plt.xlabel("Вес")
    plt.title(f"Профиль X для '{char}'")
    plt.yticks(range(0, len(profileX), max(1, len(profileX) // 10)))  # Подписи по X
    plt.xticks(range(0, max(profileX) + 1, max(1, (max(profileX) + 1) // 10)))  # Подписи по Y

    plt.subplot(1, 2, 2)
    plt.bar(range(len(profileY)), profileY)
    plt.xlabel("Y")
    plt.ylabel("Вес")
    plt.title(f"Профиль Y для '{char}'")
    plt.xticks(range(0, len(profileY), max(1, len(profileY) // 10)))
    plt.yticks(range(0, max(profileY) + 1, max(1, (max(profileY) + 1) // 10)))

    plt.tight_layout()  # Предотвращает наложение подписей
    profileFilename = f"{folderProf}/{char}Profile.png"
    plt.savefig(profileFilename)
    plt.close()

    print(f"Profiles for '{char}' are saved in {profileFilename}...\n")

csvFilename = "features.csv"
with open(csvFilename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    writer.writerow(
        [
            "character",
            "quarter_weights",
            "normalized_quarter_weights",
            "center_x",
            "center_y",
            "normalized_center_x",
            "normalized_center_y",
            "inertia_x",
            "inertia_y",
            "normalized_inertia_x",
            "normalized_inertia_y",
        ]
    )
    writer.writerows(data)

print(f"The features are saved in {csvFilename}...")

print("Everything is completed")