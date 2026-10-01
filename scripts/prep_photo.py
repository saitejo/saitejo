import sys
import numpy as np
import cv2
from rembg import remove
from PIL import Image
import io


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    with open(input_path, "rb") as f:
        input_data = f.read()
    output_data = remove(input_data)
    img = Image.open(io.BytesIO(output_data)).convert("RGBA")
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(white_bg, img)
    gray = composite.convert("L")
    arr = np.array(gray)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(arr)
    result = Image.fromarray(enhanced)
    result.save("source-prepped.png")


if __name__ == "__main__":
    main()
