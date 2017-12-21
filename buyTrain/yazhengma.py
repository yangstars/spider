# !/bin/env python
# -*- coding=utf-8 -*-
import ssl
import urllib2
i=1
import time
while(1):
    #不加的话，无法访问12306
    ssl._create_default_https_context = ssl._create_unverified_context
    # headers = {“User-Agent”: “Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36”}
    # req = urllib2.Request(“http://211.87.155.19/(yfsvlfreem4d0b553vkfzfzt)/CheckCode.aspx“, headers=headers)
    # https: // www.zhihu.com / captcha.gif?r = 1495351271125 & type = login
    req = urllib2.Request("https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.7174227166135074")
    u=urllib2.urlopen(req)
    data = u.read()
    f = open("F:/python/yanzhengma/"+str(i)+".jpg",'wb')
    print i
    time.sleep(2)#有时需要加延时，以防被封。
    i=i+1
    f.write(data)
    f.close()