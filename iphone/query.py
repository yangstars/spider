# !/bin/env python
# -*- coding=utf-8 -*-
import requests
from PIL import Image
from json import loads
from urllib import urlencode
import json
import re
import time
import datetime
from urllib import unquote
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import ssl

# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# # 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 关闭12306的安全证书验证
ssl._create_default_https_context = ssl._create_unverified_context


class Iphone(object):
    def __init__(self):
        # [*] 请输入验证码位置，以","分割[例如2,5]:4,6

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
            'Content-Type': 'text/html;charset=utf-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }
        self.session = requests.session()

 # 获取验证码图片
    def getImg(self):
        # sn=356983064087973&app_key=&disabledb=0&timestamp=&captcha=
        url = "https://act.feng.com/wetools/index.php?r=appleinfo/search"
        data ={
            'sn':'356983064087973',
            'app_key': '',
            'disabledb':'0',
            'timestamp':'',
            'captcha':''
        }
        params = urlencode(data)
        response = urllib.urlopen(url, params)
        # response = self.session.get(url=url,data=params, headers=self.headers, verify=False)
        print response.read()

        # 把验证码图片保存到本地
        # with open('img.jpg', 'wb') as f:
        #     f.write(response.content)
        #     # 用pillow模块打开并解析验证码,这里是假的，自动解析以后学会了再实现
        # try:
        #     im = Image.open('img.jpg')
        #     # 展示验证码图片，会调用系统自带的图片浏览器打开图片，线程阻塞
        #     im.show()
        #     # 关闭，只是代码关闭，实际上图片浏览器没有关闭，但是终端已经可以进行交互了(结束阻塞)
        #     im.close()
        # except:
        #     print u'[*] 请输入验证码2'
        # captcha_solution = raw_input('[*] 请输入验证码1：')
        # return captcha_solution

        # 验证结果

    def getResult(self):
        pass
#程序入口
if __name__ == '__main__':
    iphone = Iphone()
    # （1）图片验证
    yan = iphone.getImg()
    # chek = False
    # # 只有验证成功后才能执行登录操作
    # while not chek:
    #     chek = iphone.getResult(yan)