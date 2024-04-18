import os

from checkPoints import checkPoint, screenConfig
import config
from operation import *
from process import *
from KeyboardListener import Listener

import sys
import pyautogui as pi
# import pygetwindow as pw
import threading
import time
from tkinter import messagebox
import shutil



# def readOneAchievementSet(title):
#     data = process(title)
#     dfs = readExcel(name=title)
#     print(data[title])
#     merged_df, unmerged_df1, unmerged_df2 = fuzzy_merge(dfs[title].astype(str), data[title].astype(str), '名称', 'name', threshold=60)
#     merged_df = merged_df[['版本', '分类', '名称', '描述', '星琼', 'finish']]
#     print(unmerged_df1.keys())
#     if not unmerged_df1.empty:
#         unmerged_df1 = unmerged_df1[['版本', '分类', '名称', '描述', '星琼']]
#         print(unmerged_df2.keys())
#     else:
#         print("all achievements are paired")
    
#     if not unmerged_df2.empty:
#         unmerged_df2 = unmerged_df2[['name', 'finish', 'date']]
#         print(unmerged_df2.keys())
#     else:
#         print("all achievements are paired")

#     merged_df.rename(columns={'finish': '完成情况'})
#     unmerged_df1.rename(columns={'finish': '完成情况'})
#     unmerged_df2.rename(columns={'finish': '完成情况'})
#     print("可匹配的成就")
#     print(merged_df)
#     print("未完成的成就")
#     print(unmerged_df1)
#     print("未匹配的成就")
#     print(unmerged_df2)

#     return {'title': title, 'pair': merged_df, 'unfinished': unmerged_df1, 'notPair': unmerged_df2}

#     # return title

def readOneAchievementSet(dfs, title):
    interruptHandler()
    unmatchedList, df = process(title, dfs[title])
    return {'title': title, 'pair': df, "notPair": unmatchedList}

def main():
    # activate the windows and get the properties
    activateWindows("崩坏：星穹铁道")
    # activate_window = pw.getWindowsWithTitle("崩坏：星穹铁道")[0]
    # print(activate_window)
    # activate_window.minimize()
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
    # choose the center set to read
    moveMouseToCenter()
    pi.click()

    achievementList = {}
    while readSet.__len__() < config.names.keys().__len__() :
        interruptHandler()

        time.sleep(1)
        title = getTitle()
        print("正在读取：", title)
        # print(setName)
        if setName != '':
            if title != setName:
                exitSpecialAchievementSet()
                changeAchievementSet()
                continue
        if title in readSet:
            saveToExcel(achievementList)
            if not save_img:
                for key in config.names:
                    shutil.rmtree(config.names[key])
                    os.mkdir(config.names[key])
            messagebox.showinfo(title="提示", message="已完成所有成就的读取")
            config.listener_stop_flag = True
            return
        else:
            # data = readOneAchievementSet(title)
            # achievementList[title] = [data['pair'], data['unfinished'], data['notPair']]
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
                        # print(os.getcwd())
                        shutil.rmtree(config.names[key])
                        os.mkdir(config.names[key])
                messagebox.showinfo(title="提示", message="已完成所有成就的读取")
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

    # main()
