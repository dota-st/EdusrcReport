'''
Author: dota_st
Date: 2022-01-17 17:01:39
blog: www.wlhhlc.top
'''
import requests
import re
import configparser
import json
import warnings
import os
import urllib.parse
warnings.filterwarnings("ignore")
config = configparser.ConfigParser()
config.read("config.ini")

def old_file_read(file_name):
    file = open("./old_file/"+file_name, 'r', encoding="utf-8").read()
    file = urllib.parse.unquote(file)
    return file

def get_image(file_name):
    short_file_name = file_name.split(".")[0]
    file_content = old_file_read(file_name)
    img_pattern = r'(!\[.*?\]\({0}\.assets/image-.*?.png\))'.format(short_file_name)
    image_list = re.findall(img_pattern, file_content)
    return image_list

def upload_img(file_name):
    img_list = get_image(file_name)
    dir_list = []
    img_path_list = []
    for i in img_list:
        short_file_name = file_name.split(".")[0]
        img_pattern = r'({0}\.assets/image-.*?.png)'.format(short_file_name)
        dir = re.findall(img_pattern, i)
        dir_list.extend(dir)
    for i in dir_list:
        i = str(i)
        real_file = "./old_file/" + i
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "x-csrftoken": config['settings']['x-csrftoken'],
        "Connection": "close",
        "Referer": "https://src.sjtu.edu.cn/add/",
        "Cookie": config['settings']['cookie']
        }
        pattern = r"(image-.*?.png)"
        img_name = re.search(pattern, i).group()
        res = requests.post(url="https://src.sjtu.edu.cn/upload-images/", headers=headers, data={'name': img_name}, files ={"file": open(real_file,"rb")}, verify=False)
        result = json.loads(res.text)
        img_path = "https://src.sjtu.edu.cn" + result["url"]
        print(f"\033[1;35m[+]{file_name} upload success! >> \033[0m" + img_path)
        img_path_list.append(img_path)
    return img_path_list
    

def custom_make_translation(text, translation):
    regex = re.compile('|'.join(map(re.escape, translation)))
    return regex.sub(lambda match: translation[match.group(0)], text)

def create_file(file_name):
    content = old_file_read(file_name)
    img_list = get_image(file_name)
    if img_list:
        path_list = upload_img(file_name)
        dicts = dict()
        for i,j in zip(img_list,path_list):
            dicts[i]=j
        content = custom_make_translation(content, dicts)
    new_file = open("./new_file/"+file_name, 'w')
    print(f"\033[1;32m[ok]{file_name} create success!\033[0m")
    new_file.write(content)

def main():
    file_list = os.listdir("./old_file/")
    files = "  ".join(file_list)
    logo = r"""
___________    .___                          __________                             __   
\_   _____/  __| _/_ __  _____________   ____\______   \ ____ ______   ____________/  |_ 
 |    __)_  / __ |  |  \/  ___/\_  __ \_/ ___\|       _// __ \\____ \ /  _ \_  __ \   __\
 |        \/ /_/ |  |  /\___ \  |  | \/\  \___|    |   \  ___/|  |_> >  <_> )  | \/|  |  
/_______  /\____ |____//____  > |__|    \___  >____|_  /\___  >   __/ \____/|__|   |__|  
        \/      \/          \/              \/       \/     \/|__|                       

Powered by dota_st
Blog's: https://www.wlhhlc.top/
"""
    print(logo)
    print('')
    print(f"\033[1;34m[*]scan file_dir: {files}\033[0m")
    for i in file_list:
        if os.path.exists("./new_file/" + i):
            pass
        elif ".assets" in i:
            pass
        else:
            create_file(i)

if __name__ == '__main__':
    main()