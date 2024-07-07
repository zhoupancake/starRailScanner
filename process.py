import os
import pandas as pd
import random
import cv2 as cv
import pyautogui as pi
from fuzzywuzzy import process as pr
from tkinter import messagebox
from tqdm import tqdm
from tqdm._tqdm import trange

import config
from ocr import getString
from operation import screenshot, moveMouseToCenter, scroll, locationCalculate
from selector import select
from excelOperation import readExcel, saveToExcel

data = {}


def characterSegment(*, path=None, img: cv.typing.MatLike):
    if img is None and path is not None:
        img = cv.imread(path)
    elif img is None and path is None:
        print("illegal parameters passed.")
    elif img is not None and path is not None:
        img = cv.imread(path)

    strs = {"name": "", "description": "", "detail": "", "finish": "", "date": "", "notAccept": "", "notFinish": ""}
    keys = {"description": ["name", "description", "detail"], "finish": ["finish", "date", "notAccept", "notFinish"]}
    for key in keys.keys():
        for value in keys[key]:
            x1, y1, x2, y2 = locationCalculate(img.shape[1], img.shape[0], key, value)
            temp = img[y1:y2, x1:x2]
            # if value == "finish" or value == "notAccept" or value == "notFinish":
            # random_integer = random.randint(1, 10000000)
            # cv.imwrite(f"{value}{random_integer}.png", temp)
            strs[value] = getString(path=None, img=temp)
    # return strs["name"], strs["description"], strs["detail"], strs["finish"], strs["date"], strs["notAccept"], strs["notFinish"]
    if strs["finish"] == "已完成" or strs["finish"] == "completed":
        finishQ = True
    elif '/' in strs["notFinish"] or '/' in strs["notAccept"] or strs["notFinish"] == "进行中":
        finishQ = False
    else:
        print(f"unrecognized finish status: {strs["name"]}")
        finishQ = True
    return strs["name"], finishQ


def process(title: str, df):
    unmatchedList = []
    data: list[str] = []

    while True:
        interruptHandler()

        finishScreenshot = False
        moveMouseToCenter()
        pi.click()

        # 截图
        path = screenshot(title)
        imgs = select(path)

        # 读取成就并进行匹配
        if len(imgs) < 5:
            print(f"less than 5 images in the screenshot of path {path}")

        for index, img in enumerate(imgs):
            interruptHandler()

            # 识别成就名称
            for i in range(5):
                name, finishQ = characterSegment(path=None, img=img)
                if name != "":
                    if i > 0:
                        print(f"retry {i} times in #{5 - index} image")
                    break

            if name == "":
                print(f"unrecognized name in #{5 - index} image of path {path}")
                continue

            if name in data:
                print("reading achievements finished")
                finishScreenshot = True
                break

            data.append(name)
            isMatch = True
            if config.language == 'ch':
                isMatch, df = fuzzy_merge_custom(df, name, "完成情况", "名称", "已完成" if finishQ else "未完成")
            elif config.language == 'en':
                isMatch, df = fuzzy_merge_custom(df, name, "completed", "name", "completed" if finishQ else "not completed")
            if not isMatch:
                unmatchedList.append(name)

        if finishScreenshot:
            break
        moveMouseToCenter()
        pi.click()
        scroll(1)
    return unmatchedList, df


def fuzzy_merge_custom(df, target_string: str, modify_column: str, column_name: str, fillstr: str, threshold=60):
    matches = pr.extractOne(target_string, df[column_name])
    # 强制修改matches的类型标注为 tuple[str, int, int]
    import typing
    matches = typing.cast(tuple[str, int, int], matches)
    if matches[1] > threshold:
        best_match_row = df[df[column_name] == matches[0]]
        if config.language == 'ch':
            df.loc[best_match_row.index, modify_column] = "已完成"
        elif config.language == 'en':
            df.loc[best_match_row.index, modify_column] = "completed"
        return True, df
    else:
        return False, df


def getCount():
    if not os.path.exists("./imgs"):
        current_directory = os.path.dirname(__file__)
        imgs_path = os.path.join(current_directory, "imgs/")
        os.makedirs(imgs_path)
        for name in config.names:
            relative_folder_path = "/imgs/" + config.names[name]
            absolute_folder_path = os.path.join(current_directory, relative_folder_path)
            os.makedirs(absolute_folder_path)
            config.counts[name] = 0
        return
    else:
        for name in config.names:
            path = "./imgs/" + config.names[name]
            try:
                # 如果不存在文件夹，创建文件夹
                files = os.listdir(path)
            except FileNotFoundError:
                os.makedirs(path)
                config.counts[name] = 0
                continue
            fileNum = len(files)
            config.counts[name] = fileNum


def getTitle(img=None) -> str:
    global closeName
    input_string = ''
    if img is None:
        path = "./imgs/{0}/{1}.jpg".format("temp", config.counts["temp"] + 1)
        x1, y1, x2, y2 = locationCalculate(config.location["screen"]["size"][0], config.location['screen']['size'][1],
                                           "screen", "title")
        pi.screenshot(imageFilename=path, region=(x1, y1, x2 - x1, y2 - y1))
        input_string = getString(path)
    else:
        input_string = getString(img)

    closest_match = pr.extractOne(input_string, config.names.keys())
    if closest_match:
        closeName = closest_match[0]
    else:
        print("No match found.")
    return closeName


def interruptHandler():
    if config.main_stop_flag:
        if config.language == 'ch':
            messagebox.showerror(title="错误", message="键盘输入强制停止标识，脚本运行停止")
            print("键盘输入强制停止标识，脚本运行停止......")
        elif config.language == 'en':
            messagebox.showerror(title="error", message="An interrupt is listened, the execution is stopped")
            print("An interrupt is listened, the execution is stopped")
        exit()
    else:
        pass
