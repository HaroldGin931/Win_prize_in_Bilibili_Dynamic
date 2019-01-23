#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
    Bilibili动态转发抽奖脚本 Python 3 版本
    修改者信息：
    Bilibili 用户名：蝉森旅人
    Github：https://github.com/HaroldLee115

    原作者信息：
    Bilibili动态转发抽奖脚本 V1.1
    Auteur:Poc Sir   Bilibili:鸟云厂商
    Mon site Internet:https://www.hackinn.com
    Weibo:Poc-Sir Twitter:@rtcatc
    更新内容：1.增加了对画册类型动态的支持。
"""

import os
import urllib.request
import json
import sqlite3
import random
import webbrowser
import re
import time
from urllib import parse as urlparse  

def GetMiddleStr(content,startStr,endStr):
    #result = re.findall(r'\d+', str(content))
    startIndex = content.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    return content[startIndex:endIndex] #result[-1]

'''def GetMiddleStr(content,startStr,endStr):
    startIndex = content.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    return content[startIndex:endIndex]'''

def GetUsers():
    global Bilibili_Key
    GetTotalRepost()
    Tmp_count = 0
    Bilibili_Key = 0
    DynamicAPI = "https://api.live.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost?dynamic_id="+ Dynamic_id + "&offset="
    conn = sqlite3.connect('Bilibili_TMP.db')
    c = conn.cursor()
    while Tmp_count<Total_count:
        Tmp_DynamicAPI = DynamicAPI + str(Tmp_count)
        try:
            BiliJson = json.loads(GetMiddleStr(urllib.request.urlopen(Tmp_DynamicAPI).read(),b"comments\":",b",\"total"))
            for BiliJson_dict in BiliJson:
                Bilibili_UID = str(BiliJson_dict['uid'])
                Bilibili_Uname = BiliJson_dict['uname']
                Bilibili_Comment = BiliJson_dict['comment']
                Bilibili_Sql = "INSERT or REPLACE into Bilibili (UID,Uname,Comment,ID) VALUES (" + Bilibili_UID + ", '" + Bilibili_Uname + "', '" + Bilibili_Comment + "', " + str(Bilibili_Key) + ")"
                c.execute(Bilibili_Sql)
                conn.commit()
                Bilibili_Key = Bilibili_Key + 1
        except:
            break
        Tmp_count = Tmp_count + 20
    else:
        Tmp_count = 0
    conn.close()

def GetTotalRepost():
    global Total_count
    global UP_UID
    DynamicAPI = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=" + Dynamic_id
    BiliJson = json.loads(urllib.request.urlopen(DynamicAPI).read())
    Total_count = BiliJson['data']['card']['desc']['repost']
    UP_UID = BiliJson['data']['card']['desc']['user_profile']['info']['uid']

def GetLuckyDog():
    Bilibili_Doge = random.randint(0, Bilibili_Key)

    conn = sqlite3.connect('Bilibili_TMP.db')
    c = conn.cursor()
    cursor = c.execute("SELECT UID from Bilibili where ID=" + str(Bilibili_Doge))
    res = cursor.fetchall()
    suc = True
    if len(res) > 0 :
        suc = True
        cursor.close()
        conn.close()
        conn2 = sqlite3.connect('Bilibili_TMP.db')
        c2 = conn2.cursor()
        info_cursor = c2.execute("SELECT UID,Uname,Comment from Bilibili where ID=" + str(Bilibili_Doge))
        for row in info_cursor:
            print("用户ID:", row[0])
            print("用户名:", row[1])
            print("转发详情：", row[2], "\n")
            bilibili_open = input(TellTime() + "是否打开网页给获奖用户发送私信：（Y/N）");
            if bilibili_open == "Y":
                webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
            elif bilibili_open == "y":
                webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
            elif bilibili_open == "Yes":
                webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
            elif bilibili_open == "yes":
                webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
            elif bilibili_open == "是":
                webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
            elif bilibili_open == "是的":
                webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
        conn2.close()
    else:
        suc = False
        cursor.close()
        conn.close()
        GetLuckyDog()

def DeleteDatabase():
    DB_path = os.getcwd() + os.sep + "Bilibili_TMP.db"
    try:
        os.remove(DB_path)
        print (TellTime() + "正在清理缓存...")
    except:
        print (TellTime() + "正在清理缓存...")

def CreateDatabase():
    conn = sqlite3.connect('Bilibili_TMP.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE Bilibili
       (UID INT PRIMARY KEY     NOT NULL,
       Uname           TEXT    NOT NULL,
       Comment           TEXT    NOT NULL,
       ID            INT      NOT NULL);''')
    conn.commit()
    conn.close()

def GetDynamicid():
    s = input("请粘贴您获取到的网址：")
    nums = re.findall(r'\d+', s)

    #bilibili_domain = urllib.parse(s)[1]
    bilibili_domain = urlparse.urlparse(s)[1]
    #print(bilibili_domain)

    if bilibili_domain == "t.bilibili.com":
        print (TellTime() + "为纯文本类型动态")
        return str(nums[0])
    elif bilibili_domain == "h.bilibili.com":
        bilibili_docid = "https://api.vc.bilibili.com/link_draw/v2/doc/dynamic_id?doc_id=" + str(nums[0])
        Dynamic_id = GetMiddleStr(urllib.request.urlopen(bilibili_docid).read(),b"dynamic_id\":\"",b"\"}}")
        print (TellTime() + "为画册类型动态")
        return int(Dynamic_id)

def TellTime():
    localtime = "[" + str(time.strftime('%H:%M:%S',time.localtime(time.time()))) + "]"
    return localtime

if __name__ == '__main__':
    DeleteDatabase()
    print ("+------------------------------------------------------------+")
    print ("|在电脑端登录Bilibli,点击进入个人主页,再点击动态,进入动态页面|")
    print ("|点击对应的动态内容，将获取到的网址复制，并粘贴在下方：      |")
    print ("+------------------------------------------------------------+\n")
    Dynamic_id = str(GetDynamicid())
    TellTime()
    print (TellTime() + "获取动态成功，ID为：" + Dynamic_id)
    print (TellTime() + "正在获取转发数据中......")

    CreateDatabase()
    GetUsers()

    print (TellTime() + "获取数据成功！")
    #print(Bilibili_Key)
    print('总转发用户', Total_count)
    print (TellTime() + "中奖用户信息：\n")
    GetLuckyDog()
    DeleteDatabase()

