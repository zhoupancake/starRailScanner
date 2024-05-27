import os
import pytesseract as pt
try:
    from PIL import Image, ImageChops
except ImportError:
    import Image

import config

def configuration():
    os.environ['TESSDATA_PREFIX'] = config.TESSDATA_PREFIX
    pt.pytesseract.tesseract_cmd = config.TESSDATA_PATH

def getString(path="./imgs/temp/temp.jpg", img=None):
    if os.environ.get("TESSDATA_PREFIX") is None:
        configuration()
    if img is None and path is not None:
        img = Image.open(path)
    elif img is None and path is None:
        print("illegal parameters passed.")
    elif img is not None and path is not None:
        img = Image.open(path)
    config_str = ''
    if config.language == 'ch':
        config_str = '-l chi_sim --oem 1 --psm 6'
    elif config.language == 'en':
        config_str = '-l eng --oem 1 --psm 6'
    text = pt.image_to_string(img, config=config_str)
    return text.replace("\n", "")
