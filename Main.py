import os

import sys
import pyautogui as pi
import threading
import time
from tkinter import messagebox
import shutil

from checkPoints import checkPoint, screenConfig
import config
from operation import *
from process import *
from KeyboardListener import Listener


def readOneAchievementSet(dfs, title):
    interruptHandler()
    unmatchedList, df = process(title, dfs[title])
    return {'title': title, 'pair': df, "notPair": unmatchedList}


def main():
    # activate the windows and get the properties
    window_name = "崩坏：星穹铁道" if config.language == 'ch' else 'Honkai: Star Rail'
    activateWindows(window_name)
    getCount()

    setName = ''
    update_way = ''
    if len(sys.argv) > 1:
        setName = sys.argv[1]
        if len(sys.argv) > 2:
            update_way = sys.argv[2]
    if setName not in config.names.keys():
        setName = ''
    readSet = []
    moveMouseToCenter()
    pi.click()

    achievementList = {}
    while readSet.__len__() < config.names.keys().__len__():
        interruptHandler()

        time.sleep(1)
        title = getTitle()
        if config.language == 'ch':
            print("正在读取：", title)
        elif config.language == 'en':
            print("reading set: ", title)
        if setName != '':
            if title != setName:
                exitSpecialAchievementSet()
                changeAchievementSet()
                continue
        if title in readSet:
            saveToExcel(achievementList)
            if not config.save_img:
                for key in config.names:
                    shutil.rmtree(config.names[key])
                    os.mkdir(config.names[key])
            if config.language == 'ch':
                messagebox.showinfo(title="提示", message="已完成所有成就的读取")
            elif config.language == 'en':
                messagebox.showinfo(title="tips", message="reading finished")
            config.listener_stop_flag = True
            return
        else:
            dfs = readExcel()
            data = readOneAchievementSet(dfs, title)
            achievementList[title] = data
            if setName != '' and (update_way == 'u' or update_way == ''):
                for key in dfs:
                    interruptHandler()

                    if key != title:
                        notProcess_df = {'title': key, 'pair': dfs[key], "notPair": None}
                        achievementList[key] = notProcess_df
            readSet.append(title)
            if setName != '':
                saveToExcel(achievementList)
                if not config.save_img:
                    os.chdir(r"./imgs")
                    for key in config.names:
                        shutil.rmtree(config.names[key])
                        os.mkdir(config.names[key])
                if config.language == 'ch':
                    messagebox.showinfo(title="提示", message="已完成所有成就的读取")
                elif config.language == 'en':
                    messagebox.showinfo(title="tips", message="reading finished")
                config.listener_stop_flag = True
                return
            exitSpecialAchievementSet()
            changeAchievementSet()


if __name__ == "__main__":
    # checking the basic setting of the python environment and screen
    if not checkPoint() or not screenConfig():
        exit()

    config.listener_stop_flag = False
    config.main_stop_flag = False
    main_thread = threading.Thread(target=main)
    listener_thread = threading.Thread(target=Listener)
    listener_thread.start()
    main_thread.start()

    main_thread.join()
    listener_thread.join()

