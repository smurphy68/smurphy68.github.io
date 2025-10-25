import requests
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import imagehash


image_width = 488
image_height = 680


def display_image_with_phash(url, definition=1):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    w, h = image.size

    wi = int(round(w / definition, 0))
    hi = int(round(h / definition, 0))
    transformed_image = image.convert("L").resize((wi, hi), Image.Resampling.LANCZOS)
    phash_value = imagehash.phash(transformed_image, hash_size=64)

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    ax[0].imshow(image)
    ax[0].set_title("Original Image")
    ax[0].axis("off")

    ax[1].imshow(transformed_image, cmap="gray")
    ax[1].set_title("Transformed for pHash")
    ax[1].axis("off")

    plt.show()

    return str(phash_value)


def convert_image_url_to_phash(url, definition=1):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    w, h = image.size

    wi = int(round(w / definition, 0))
    hi = int(round(h / definition, 0))
    transformed_image = image.convert("L").resize((wi, hi), Image.Resampling.LANCZOS)
    phash_value = imagehash.phash(transformed_image, hash_size=16)
    phash_bitewise = int(str(phash_value), 16).to_bytes(32, byteorder="big")

    return phash_bitewise


def phash_clip(pil_image, definition=1):
    wi = int(round(image_width / definition, 0))
    hi = int(round(image_height / definition, 0))
    transformed_image = pil_image.convert("L").resize((wi, hi), Image.Resampling.LANCZOS)
    phash_value = imagehash.phash(transformed_image, hash_size=16)
    phash_bitewise = int(str(phash_value), 16).to_bytes(32, byteorder="big")

    return phash_bitewise
