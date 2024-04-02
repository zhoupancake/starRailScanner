import os
from config import *
import pytesseract as pt
try:
    from PIL import Image, ImageChops
except ImportError:
    import Image

def configuration():
    os.environ['TESSDATA_PREFIX'] = TESSDATA_PREFIX
    pt.pytesseract.tesseract_cmd = TESSDATA_PATH

def getString(path="./imgs/temp/temp.jpg", img=None):
    if os.environ.get("TESSDATA_PREFIX") is None:
        configuration()
    if img is None and path is not None:
        img = Image.open(path)
    elif img is None and path is None:
        print("illegal parameters passed.")
    elif img is not None and path is not None:
        img = Image.open(path)
    config = ('-l chi_sim --oem 1 --psm 6')
    text = pt.image_to_string(img, config=config)
    return text.replace("\n", "")

# def different(path1, path2):
#     img1 = Image.open(path1).convert('L')
#     img2 = Image.open(path2).convert('L')
#     print(path1," ", path2)
#     diff = ImageChops.difference(img1, img2)
#     diff.save("final.jpg")
#     print(diff.getbbox())
#
#     return diff.getbbox() is not None

if __name__ == "__main__":
    print(getString("./notAccept2934095.png"))
