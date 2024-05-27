import os
import importlib
import pyautogui as pi

import config

def check_package_installed(package_name):
    try:
        importlib.import_module(package_name)
    except ImportError:
        return False
    else:
        return True


def checkPoint():
    package_name = ["fuzzywuzzy", "numpy", "cv2", "pandas", "pyautogui", "pygetwindow", "pytesseract"]
    checkPass = True
    
    for name in package_name:
        if not check_package_installed(name):
            print("The package", name, "is not installed.")
            checkPass = False
    
    return checkPass

def checkStructure():
    path = "./imgs"
    if not os.path.exists(path):
        os.makedirs(path)
        os.chdir(path)
        for value in config.names.values:
            os.makedirs(path+"/"+value)
        os.chdir("..")


def screenConfig():
    pi.PAUSE = 0.1
    pi.FAILSAFE = False
    screenSize = pi.size()
    # if screenSize.height == 1600 and screenSize.width == 2560:
    screenSize_str = str(screenSize.width) + "*" + str(screenSize.height) + "_" + config.language
    if screenSize_str in config.location_list.keys():
        config.location = config.location_list[screenSize_str]
        print("分辨率检测通过")
        return True
    else:
        print("分辨率错误")
        return False