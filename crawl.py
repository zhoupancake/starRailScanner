import re
import pandas as pd
import os
import sys
import requests

import config


def acquire_html_online(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
        }
        html_temp = requests.get(url, headers=headers)
        html_temp.encoding = html_temp.apparent_encoding
        html = html_temp.text
        return html
    except BaseException:
        if config.language == "en":
            print("fail to crawl the html code")
        elif config.language == "ch":
            print("爬取网页失败")
        elif config.language == "ja":
            print("ページの取得に失敗しました")


def split_without_comma(match_str):
    key_value_pairs = re.findall(r'([^:]+):((?:[^,"]+|"[^"]*")+)', match_str)
    result = []
    for key, value in key_value_pairs:
        result.append((key.replace(',', ''), value))
    return result


def html2dataFrame(html_str):
    df = pd.DataFrame(columns=['id', 'series', 'series_name', 'series_index',
                               'name', 'description', 'currency', 'hidden', 'version',
                               'gacha', 'timegated', 'missable', 'impossible', 'percent', 'note'])

    achievements_str_all = html_str.split("achievement_groups:[")
    for i in range(1, len(achievements_str_all)):
        achievements_str_set = achievements_str_all[i].split(']}]}')[0]
        achievements_str_set = achievements_str_set.split(']},')
        for j in range(len(achievements_str_set)):
            count = achievements_str_set[j].count('id:')
            achievement_str = achievements_str_set[j].split('achievements:[')[1]

            achievements_str = achievement_str.split('},')

            for n in range(count):
                achievement_str = achievements_str[n].replace('{', '')
                achievement_str = achievement_str.replace('}', '')
                achievement_attributes = split_without_comma(achievement_str)
                if achievement_attributes[9][0] == 'difficulty':
                    del achievement_attributes[9]
                if achievement_attributes[9][0] == 'video':
                    del achievement_attributes[9]

                achievement_list = []
                if config.language == "en":
                    for k in range(len(achievement_attributes)):
                        value = achievement_attributes[k][1]
                        value = value.strip('"')
                        value = value.strip('\'')
                        value = value.replace('\\\\nâ\x80» ', ' ※')
                        value = value.replace('nâ\x80»', '')
                        value = value.replace('\\nâ»', '')
                        value = value.replace('\\', '')
                        achievement_list.append(value)
                elif config.language == "ch":
                    for k in range(len(achievement_attributes)):
                        value = achievement_attributes[k][1]
                        value = value.strip('"')
                        value = value.strip('\'')
                        value = value.replace('\\n', '')
                        value = value.replace('false', '')
                        value = value.replace('true','隐藏')
                        value = value.replace(' ', '')
                        value = value.replace('TEXTJOIN#87','晖长石号/开拓之尾号/塔塔洛夫号/飞翔时针号')
                        value = value.replace('[m]','万')
                        value = value.replace('TEXTJOIN#54','扑满')
                        achievement_list.append(value)
                elif config.language == "ja":
                    for k in range(len(achievement_attributes)):
                        value = achievement_attributes[k][1]
                        value = value.strip('"')
                        value = value.strip('\'')
                        value = value.replace('\\n', '')
                        value = value.replace('false', '')
                        value = value.replace('true', '隠れる')
                        value = value.replace(' ', '')
                        value = value.replace('TEXTJOIN#87','暉長石号')
                        value = value.replace('[m]','万')
                        value = value.replace('TEXTJOIN#54','プーマン')
                        achievement_list.append(value)
                if count == 1:
                    if config.language == "en":
                        achievement_list.append('None')
                    elif config.language == "ch":
                        achievement_list.append('无')
                    elif config.language == "ja":
                        achievement_list.append('なし')
                else:
                    if config.language == "en":
                        achievement_list.append('{0} combined'.format(count))
                    elif config.language == "ch":
                        achievement_list.append('{0}选一'.format(count))
                    elif config.language == "ja":
                        achievement_list.append('{0} combined'.format(count))
                df.loc[len(df.index)] = achievement_list
    df = df.loc[:, ['series_name', 'name', 'description', 'currency', 'hidden', 'version', 'note']]
    if config.language == "en":
        df.insert(loc=2, column='completed', value='false')
    elif config.language == "ch":
        df.insert(loc=2, column='completed', value='未完成')
    elif config.language == "ja":
        df.insert(loc=2, column='completed', value='未完了')
    df = df.rename(columns={'series_name': 'series', 'currency': 'jades'})
    df = df[['version', 'series', 'name', 'description', 'jades', 'hidden', 'note', 'completed']]
    if config.language == "ch":
        df = df.rename(columns={'version': '版本', 'series': '分类', 'name': '名称', 'description': '描述', 'jades' : '星琼', 'hidden':'隐藏', 'note' : '备注', 'completed' : '完成情况'})
    elif config.language == "ja":
        df = df.rename(columns={'version': 'バージョン', 'series': '分類', 'name': '名称', 'description': '説明', 'jades' : '星玉', 'hidden':'隠れる', 'note' : '備考', 'completed' : '完了状況'})
    return df


def dataFrame2Excel(df):
    grouped = None
    if config.language == "en":
        grouped = df.groupby('series')
        with pd.ExcelWriter('./achievementSet_full/2.4_en.xlsx') as writer:
            for group_name, group_data in grouped:
                group_data.to_excel(writer, sheet_name=group_name, index=False)
    elif config.language == "ch":
        grouped = df.groupby('分类')
        with pd.ExcelWriter('./achievementSet_full/2.4_ch.xlsx') as writer:
            for group_name, group_data in grouped:
                group_data.to_excel(writer, sheet_name=group_name, index=False)
    elif config.language == "ja":
        grouped = df.groupby('分類')
        with pd.ExcelWriter('./achievementSet_full/2.4_ja.xlsx') as writer:
            for group_name, group_data in grouped:
                group_data.to_excel(writer, sheet_name=group_name, index=False)


if __name__ == "__main__":
    language = config.language if config.language == "en" or config.language == "ja" else "zh-cn"
    html_str = acquire_html_online("https://stardb.gg/" + language + "/achievement-tracker")
    df = html2dataFrame(html_str)
    dataFrame2Excel(df)



