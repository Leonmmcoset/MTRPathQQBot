# -*- coding: utf-8 -*- #
# 这破玩意居然不让输出URL！！！
import os
import requests
import mtrpath as mp
import mtrpath_beta as mpb

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message
from botpy.types.message import MarkdownPayload, MessageMarkdownParams
from plugins import weather_api,img_upload,fortune_by_sqlite,user_todo_list
from enum import Enum
from io import BytesIO
from math import gcd, sqrt
from operator import itemgetter
from threading import Thread, BoundedSemaphore
from time import gmtime, strftime, time
from typing import Optional, Dict, Literal, Tuple, List, Union
from queue import Queue
import base64
import json
import os
import pickle
import re
import time

from fontTools.ttLib import TTFont
from opencc import OpenCC
from PIL import Image, ImageDraw, ImageFont
import networkx as nx
import requests
test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

# api_response = requests.get('https://api.imlazy.ink/mcapi/?host=leonmmcoset.jjmm.ink&port=7180&type=json')
# status_data = api_response.json()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"机器人启动完成！")

    #判断数据库初是否始化
    fortune_by_sqlite.database_initialized()

    async def on_group_at_message_create(self, message: GroupMessage):
        msg = message.content.strip()
        member_openid = message.author.member_openid
        _log.info("bot 收到消息：" + message.content)
        if msg.startswith("/go"):
            if msg == '/go':
                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content="格式：/go [起点];[终点]\n请输入站点的全称（例如村庄|Village）\n查询最少需要3秒钟")
            elif msg == '/go ':
                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content="格式：/go [起点];[终点]\n请输入站点的全称（例如村庄|Village）\n查询最少需要3秒钟")
            else:
                _log.info('开始处理导航')
                # 去除 /go 及可能的后续空格
                input_content = msg[3:].strip()
                # 查找分号的位置
                semicolon_index = input_content.find(';')
                if semicolon_index != -1:
                    try:
                        # 提取第一个变量，去除前后空格
                        starta = input_content[:semicolon_index].strip()
                        # 提取第二个变量，去除前后空格
                        enda = input_content[semicolon_index + 1:].strip()
                        if starta != enda:
                            mpb.run(starta,enda)
                            _log.info('开始处理上传')
                            file_url = img_upload.upload('temp.jpg')  # 此处填写你要上传图片的地址
                            # file_url = f"https://s21.ax1x.com/2024/12/08/pA7DmAP.jpg"  # 这里需要填写上传的资源Url
                            messageResult = await message._api.post_group_file(
                                group_openid=message.group_openid,
                                file_type=1,  # 文件类型要对应上，具体支持的类型见方法说明
                                url=file_url  # 文件Url
                            )
                            # 资源上传后，会得到Media，用于发送消息
                            await message._api.post_group_message(
                                group_openid=message.group_openid,
                                msg_type=7,  # 7表示富媒体类型
                                msg_id=message.id,
                                media=messageResult
                            )
                            img_upload.delete_img()  # 从图床中删除图片，防止重复上传
                        else:
                            messageResult = await message._api.post_group_message(
                                group_openid=message.group_openid,
                                msg_type=0,
                                msg_id=message.id,
                                content=f"起始站和终点站不能相同！")
                    except Exception as EXCEPT:
                        _log.error(EXCEPT)
                        messageResult = await message._api.post_group_message(
                            group_openid=message.group_openid,
                            msg_type=0,
                            msg_id=message.id,
                            content=f"代码又出错了！\n这是错误：{EXCEPT}\n可能是输入的站点不正确。")
                else:
                    messageResult = await message._api.post_group_message(
                        group_openid=message.group_openid,
                        msg_type=0,
                        msg_id=message.id,
                        content="格式不正确，输入/go以获得格式！")

        _log.info(messageResult)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents, is_sandbox=True)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
