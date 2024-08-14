import pyautogui as pi
import pygetwindow as gw
import math
import time

import config


def activateWindows(title_name):
    try:
        window = gw.getWindowsWithTitle(title_name)
        window[0].activate()
    except BaseException:
        if config.language == 'ch':
            print("未检测到", title_name, "请打开后重试")
            print("打开的窗口：")
        elif config.language == 'en':
            print("can not detect window named ", title_name, ", please open the window and retry later")
            print("opening windows: ")
        for window in gw.getWindowsWithTitle(''):
            print(window.title)
        return False
    else:
        if config.language == 'ch':
            print("检测到目标窗口")
        elif config.language == 'en':
            print("detected target windows")
        return True


def screenshot(kind):
    path = "./imgs/{0}/{1}.jpg".format(config.names[kind], config.counts[kind] + 1)
    x1, y1, x2, y2 = locationCalculate(config.location["screen"]["size"][0], config.location['screen']['size'][1],
                                       "screen", "screen")
    pi.screenshot(imageFilename=path, region=(x1, y1, x2 - x1, y2 - y1))
    config.counts[kind] = config.counts[kind] + 1
    return path


def moveMouseToCenter(duration=0.1):
    x, y = pi.size()
    pi.moveTo(x / 2, y / 2, duration)


def scroll(type=1):
    # provide two types of the scroll: scroll the achievements list or change the achievements set
    # type is decided based on the passed parameter
    print("scroll", config.location['scroll'][f"type{type}_time"], config.location['scroll'][f"type{type}_length"])
    for i in range(config.location['scroll'][f"type{type}_time"]):
        pi.scroll(config.location['scroll'][f"type{type}_length"])
    time.sleep(0.3)


def changeAchievementSet():
    x, y = pi.size()
    pi.moveTo(x / 4, y / 4, 0.1)
    pi.click()
    moveMouseToCenter()
    scroll(2)
    pi.click()


def exitSpecialAchievementSet():
    x, y = pi.size()
    pi.moveTo(x * config.location["exit"][0] / 100, y * config.location["exit"][1] / 100, 0.1)
    pi.click()


def locationCalculate(w, h, kind, type):
    x1 = math.ceil(config.location[kind][type][0][0] * w / 100)
    y1 = math.ceil(config.location[kind][type][0][1] * h / 100)
    x2 = math.ceil(config.location[kind][type][1][0] * w / 100)
    y2 = math.ceil(config.location[kind][type][1][1] * h / 100)
    return x1, y1, x2, y2