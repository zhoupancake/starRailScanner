import importlib
import pyautogui as pi

def check_package_installed(package_name):
    try:
        importlib.import_module(package_name)
    except ImportError:
        return False
    else:
        return True


def checkPoint():
    package_name = ["numpy", "cv2", "PIL", "pyautogui", "pygetwindow", "math", "pytesseract", "pandas"]
    checkPass = True
    
    for name in package_name:
        if not check_package_installed(name):
            print("The package", name, "is not installed.")
            checkPass = False
    
    return checkPass


def screenConfig():
    pi.PAUSE = 0.1
    pi.FAILSAFE = False
    screenSize = pi.size()
    if screenSize.height == 1600 and screenSize.width == 2560:
        print("分辨率检测通过")
        return True
    else:
        print("分辨率错误")
        return False