import pyautogui as pi
import pygetwindow as gw
import math

from config import *

def activateWindows(title_name):
    try:
        window = gw.getWindowsWithTitle(title_name)[0]
        window.activate()
    except BaseException:
        print("未检测到", title_name, "请打开后重试")
        print("打开的窗口：")
        for window in gw.getWindowsWithTitle(''):
            print(window.title)
    else: 
        print("成功打开")

def screenshot(kind):
    path = "./imgs/{0}/{1}.jpg".format(names[kind], counts[kind]+1)
    x1, y1, x2, y2 = locationCalculate(location["screen"]["size"][0], location['screen']['size'][1], "screen", "screen")
    pi.screenshot(imageFilename=path, region=(x1, y1, x2-x1, y2-y1))
    # pi.screenshot(imageFilename=path,region=[179, 177, 2315, 1317])
    counts[kind] = counts[kind] + 1
    return path

def moveMouseToCenter(duration = 0.1):
    x , y = pi.size()
    pi.moveTo(x/2, y/2, duration) 

def scroll(len, scrollTime=SCROLL_VALUE):
    for i in range(math.floor(scrollTime + len*0.05)):
        pi.scroll(-95)
    # print("滚动切换成功")

def changeAchievementSet():
    x , y = pi.size()
    pi.moveTo(x/4, y/4, 1.0) 
    pi.click()
    moveMouseToCenter()
    scroll(0,5)
    pi.click()

def exitSpecialAchievementSet():
    x , y = pi.size()
    pi.moveTo(x*location["exit"][0]/100, y*location["exit"][1]/100, 1.0)
    pi.click()

def locationCalculate(w, h, kind, type):
    x1 = math.ceil(location[kind][type][0][0]*w/100)
    y1 = math.ceil(location[kind][type][0][1]*h/100)
    x2 = math.ceil(location[kind][type][1][0]*w/100)
    y2 = math.ceil(location[kind][type][1][1]*h/100)
    return x1, y1, x2, y2
