# !/bin/env python
# -*- coding=utf-8 -*-
import ssl
import urllib2
import time
import hashlib
from PIL import Image
from os import listdir

# ***********************  12306 验证码下载 **************************
# ***********************  12306 验证码下载 **************************
# ***********************  12306 验证码下载 **************************

def download():
    i = 1
    while(1):
        #不加的话，无法访问12306
        ssl._create_default_https_context = ssl._create_unverified_context
        # headers = {“User-Agent”: “Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36”}
        # req = urllib2.Request(“http://211.87.155.19/(yfsvlfreem4d0b553vkfzfzt)/CheckCode.aspx“, headers=headers)
        # https: // www.zhihu.com / captcha.gif?r = 1495351271125 & type = login
        req = urllib2.Request("https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.7174227166135074")
        u=urllib2.urlopen(req)
        data = u.read()
        f = open("tupian/"+str(i)+".png",'wb')
        print i
        time.sleep(2)#有时需要加延时，以防被封。
        i=i+1
        f.write(data)
        f.close()


#去重
def delete():
    # i=1
    # while(i<12):
    #     # image_file = open("tupian/" + str(i) + ".png", 'r').read()
        image_file = open("F:/python/workspace/spider/buyTrain/tupian/4.png").read()
        hashcode = hashlib.md5(image_file).hexdigest()
        print "第张图的hash值=%s"%(hashcode)
        # i+=1

if __name__ == '__main__':
    # download()
    delete()

