import os
import pandas as pd
import random
import cv2 as cv
import pyautogui as pi
from fuzzywuzzy import process as pr
from tkinter import messagebox

import config
from ocr import getString
from operation import screenshot, moveMouseToCenter, scroll, locationCalculate
from selector import select



data = {}
def characterSegment(path=None, img=None):
    if img is None and path is not None:
        img = cv.imread(path)
    elif img is None and path is None:
        print("ilegal parameters passed.")
    elif img is not None and path is not None:
        img = cv.imread(path)
    
    strs = {"name":"", "description":"", "detail":"", "finish":"", "date":"", "notAccept":"", "notFinish":""}
    keys = {"description":["name", "description", "detail"], "finish":["finish", "date", "notAccept", "notFinish"]}
    for key in keys.keys():
        for value in keys[key]:
            x1, y1, x2, y2 = locationCalculate(img.shape[1], img.shape[0], key, value)
            temp = img[y1:y2, x1:x2]
            # if value == "finish" or value == "notAccept" or value == "notFinish":
                # random_integer = random.randint(1, 10000000)
                # cv.imwrite(f"{value}{random_integer}.png", temp)
            strs[value] = getString(path=None, img=temp)
    # return strs["name"], strs["description"], strs["detail"], strs["finish"], strs["date"], strs["notAccept"], strs["notFinish"]
    return strs["name"]

# def process(title):
#     if title not in data:
#         column_names = ['name', 'description', 'detail', 'finish', 'date', 'notAccept', 'notFinish']
#         df = pd.DataFrame(columns=column_names)
#         data[title] = df 
    
#     while True:
#         finishScreenshot = False
#         moveMouseToCenter()
#         pi.click()
#         path = screenshot(title)
#         print("screenshot is finished, the path is ", path)
#         imgs = select(path)
#         print(imgs.__len__())
#         if data.__len__() > 60 and imgs.__len__() < 5:
#             moveMouseToCenter()
#             scroll(0, 4)
#             continue
#         print("select finished")
#         for img in imgs:
#             name, description, detail, finish, date, notAccept, notFinish = characterSegment(path=None, img=img)
#             print(data[title]['name'])
#             print(name)

#             # print(data[title]['name'].str.contains(name))
#             # if (not (data[title]['name'].isnull().all())) and data[title]['name'].str.contains(name, regex=False).any():
#             if (not data[title]['name'].isnull().all()) and (data[title]['name'] == name).any():
#                 print("reading achievements finished")
#                 finishScreenshot = True
#                 break
#             else:
#                 data[title] = data[title]._append({'name': name, 'description': description, 'detail': detail, 'finish': finish, 'date':date, 'notAccept': notAccept, 'notFinish': notFinish}, ignore_index=True)
#         if finishScreenshot:
#             break
#         moveMouseToCenter()
#         pi.click()
#         scroll(data.__len__())
    
#     return data

def process(title, df):
    unmatchedList = []
    data = []
    while True:
        interruptHandler()

        finishScreenshot = False
        moveMouseToCenter()
        pi.click()
        path = screenshot(title)
        # print("screenshot is finished, the path is ", path)
        imgs = select(path)
        # print(imgs.__len__())
        if data.__len__() > 60 and imgs.__len__() < 5:
            moveMouseToCenter()
            scroll(2)
            continue
        # print("select finished")
        for img in imgs:
            interruptHandler()

            name = characterSegment(path=None, img=img)
            if name in data:
                print("reading achievements finished")
                finishScreenshot = True
                break

            data.append(name)
            # print(data)
            # print(name in data)

            isMatch, df = fuzzy_merge_custom(df, name, "完成情况", "名称")
            if not isMatch:
                unmatchedList.append(name)
        if finishScreenshot:
            break
        moveMouseToCenter()
        pi.click()
        scroll(1)
    return unmatchedList, df

# def fuzzy_merge(df1, df2, left_on, right_on, threshold=60):
#     merged_df1 = []
#     unmatched_df1 = []
#     unmatched_df2 = []
#     for idx1, row1 in df1.iterrows():
#         left_value = row1[left_on]
#         match = pr.extractOne(left_value, df2[right_on], scorer=fuzz.partial_ratio)
#         if match[1] > threshold:
#             idx2 = df2.index[df2[right_on] == match[0]][0]
#             merged_row = row1.to_dict()
#             merged_row.update(df2.loc[idx2].to_dict())
#             merged_df1.append(merged_row)
#         else:
#             unmatched_df1.append(row1.to_dict())

#     for idx2, row2 in df2.iterrows():
#         right_value = row2[right_on]
#         match = pr.extractOne(right_value, df1[left_on], scorer=fuzz.partial_ratio)
#         if match[1] <= threshold:  # 反向检查未匹配的行
#             unmatched_df2.append(row2.to_dict())

#     return pd.DataFrame(merged_df1), pd.DataFrame(unmatched_df1), pd.DataFrame(unmatched_df2)

def fuzzy_merge_custom(df, target_string, modify_column, column_name, threshold=60):
    matches = pr.extractOne(target_string, df[column_name])
    # print(matches)
    if matches[1] > threshold:
        # print(type(df[column_name]))
        best_match_row = df[df[column_name] == matches[0]]
        df.loc[best_match_row.index, modify_column] = "已完成"
        return True, df
    else:
        return False, df
    
def getCount():
    for name in config.names:
        path = "./imgs/" + config.names[name]
        files = os.listdir(path)
        fileNum = len(files)
        config.counts[name] = fileNum

def getTitle(img=None):
    global closeName
    input_string = ''
    if img is None:
        path = "./imgs/{0}/{1}.jpg".format("temp", config.counts["temp"]+1)
        x1, y1, x2, y2 = locationCalculate(config.location["screen"]["size"][0], config.location['screen']['size'][1], "screen","title")
        # print("title ",x1, y1, x2, y2)
        # exit()
        pi.screenshot(imageFilename=path, region=(x1, y1, x2-x1, y2-y1))
        # pi.screenshot(imageFilename=path, region=(198,180,307,48))
        input_string = getString(path)
    else:
        input_string = getString(img)
    closest_match = pr.extractOne(input_string, config.names.keys())
    if closest_match:
        closeName = closest_match[0]
    else:
        print("No match found.")
    return closeName

def readExcel(path=config.ACHIEVEMENTS_FILE):
    # 读取 Excel 文件
    xlsx_file = pd.ExcelFile(path)
    dfs = {}

    for sheet_name in xlsx_file.sheet_names:
        dfs[sheet_name] = xlsx_file.parse(sheet_name)

    # del dfs['总目录']
    return dfs

def saveToExcel(dfs):
    writer = pd.ExcelWriter('achievements.xlsx', engine='xlsxwriter')

    for key in dfs:
        data = dfs[key]
        data['pair'].to_excel(writer, sheet_name=key, startrow=0, index=False)
        df = pd.DataFrame(data['notPair'], columns=['未匹配成就'])
        df.to_excel(writer, sheet_name=key, startrow=len(data['pair'])+2, index=False)

    writer._save()

def interruptHandler():
    if config.main_stop_flag:
        messagebox.showerror(title="错误", message="键盘输入强制停止标识，脚本运行停止")
        print("键盘输入强制停止标识，脚本运行停止......")
        exit()
    else:
        pass

if __name__ == "__main__":
    data = {
        "版本": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        "分类": ["众秘探奇", "众秘探奇", "众秘探奇", "众秘探奇", "众秘探奇", "众秘探奇", "众秘探奇", "众秘探奇", "众秘探奇", "众秘探奇", "众秘探奇", "众秘探奇"],
        "名称": [
            "直到光芒把我们带走",
            "不开放世界",
            "仙路去何通",
            "游踪遐远",
            "角色扮演游戏里合法",
            "那么代价是什么？",
            "浮财小事",
            "财星临照",
            "毁灭的冲动",
            "自由毁灭意志",
            "攻其不备",
            "身背无眼",
        ],
        "描述": [
            "激活空间站「黑塔」5个界域定锚",
            "激活贝洛伯格14个界域定锚",
            "激活仙舟「罗浮」10个界域定锚",
            "在仙舟「罗浮」激活20次界域定锚",
            "开启30次空间站「黑塔」战利品",
            "开启110次贝洛伯格战利品",
            "开启100次仙舟「罗浮」战利品",
            "在仙舟「罗浮」开启170次战利品",
            "击碎100个可破坏物",
            "击碎1000个可破坏物",
            "使用对应属性的攻击进入战斗100次",
            "在探索中遇袭",
        ],
        "星琼": [5, 5, 5, 5, 20, 20, 5, 10, 5, 10, 5, 5],
        "备注": ["无", "无", "无", "无", "无", "无", "无", "无", "无", "无", "无", "无"],
        "完成情况": ["未完成", "未完成", "未完成", "未完成", "未完成", "未完成", "未完成", "未完成", "未完成", "未完成", "未完成", "未完成"]
    }

    df = pd.DataFrame(data)

    # 给定的字符串
    given_string = "财星临照"

    isPass, matches = fuzzy_merge_custom(df, given_string, "名称", 60)

    # 返回修改的成功情况以及dataframe
    success_message = f"成功将行“{matches}”的“完成情况”一列修改为“已完成”。"
    print(df)
            
        

            