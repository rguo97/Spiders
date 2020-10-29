import time
import requests
import json
import urllib.request
import os

class Log():

    def __init__(self, level=None, message=None):
        self.get_time()
        self.get_level(level=level)
        self.get_message(message=message)

    def write_log(self):
        f = open("D://Timing//Log//log.txt", "a")
        f.write(self.time + "  "  + self.level + "  " + self.message + "\n")
        f.close()

    def get_time(self):
        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


    def get_level(self, level):
        self.level = level.upper()

    def get_message(self, message):
        self.message = message


def print_log(level,message):
    log=Log(level=level,message=message)
    log.write_log()

class Logging:
    LOG_LEVEL = ["ERROR", "INFO", "WORNING", ]
    LOG_INCLUDE = ["ippool",]


print_log("info","start to load bing picture")
file_path = "D://Timing//Bing"

nc = int(time.time()*1000)
url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=%s&pid=hp"%nc
try:
    page_text = requests.get(url).text
    print_log("info","background has gotten successfully")
except Exception as e:
    print_log("error","background has gotten failed because %s"%str(e))

image_url = json.loads(page_text)["images"][0]["url"]

image_url = "https://cd.bing.com"+image_url

image = requests.get(image_url)
local_time = time.strftime("%Y"+"%m"+"%d")
file_name = file_path+"//"+local_time+".png"





image_list = os.listdir(file_path)
time_list = []
for image in image_list:
    time_list.append(int(image[0:8]))


if len(time_list)<10:
    if int(local_time) in time_list:
        print_log("error","%s.png is in this list"%str(local_time))
    else:
        urllib.request.urlretrieve(image_url, file_name)
        print_log("info","%s.png load successfully"%str(local_time))
else:
    print_log("error","picture number more than 10")
    os.remove(file_path+"//"+str(min(time_list))+".png")
    print_log("info","%s.png has been removed successfully")
    urllib.request.urlretrieve(image_url, file_name)
    print_log("info", "%s.png load successfully" % str(local_time))
print_log("info","load bing picture is ending")
