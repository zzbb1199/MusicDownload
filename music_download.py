"""
音乐爬取器
"""
import os
from time import sleep

import requests
import json


def get_music_names(name_path, downloaded_path):
    """ 得到还没有下载的音乐名单
    :param name_path: 全部音乐名
    :param downloaded_path: 已经下载的文件
    :return:
    """
    with open(name_path, "r") as f:
        name_list = f.read()

    # 得到音乐名单
    music_names = name_list.split("\n")
    print("perpare music name", music_names)
    # 找到已经下载的文件名
    # index=2代表非目录名
    downloaded_musics = next(os.walk(downloaded_path))[2]
    print("have downloaded", downloaded_musics)
    # 排非除已经存在的名字
    music_names = list(filter(lambda x:
                              downloaded_musics.count(x + ".mp3") == 0,
                              music_names))
    print("after filter", music_names)
    # 返回需要下载的文件名
    return music_names


if __name__ == '__main__':
    # 初始化参数
    music_names = get_music_names("./music_names.txt", "./musics")
    url = 'http://www.guqiankun.com/tools/music/'
    body = {'filter': 'name', 'input': '', 'page': '1', 'type': 'netease'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.3',
        'X-Requested-With': 'XMLHttpRequest'}

    for name in music_names:
        try:
            body["input"] = name
            # 得到response 并转为 json
            data = requests.post(url, data=body, headers=headers).text
            data = json.loads(data)
            # 音乐link
            link = data["data"][0]["url"]
            if link == "" or link == None:
                continue
            # 下载音乐
            music_response = requests.get(link, headers=headers)
            # 下载
            with open("./musics/" + name + ".mp3", "wb") as file:
                file.write(music_response.content)
            print(name, "下载完成")
            sleep(2)
        except Exception as e:
            print(e)
            continue
