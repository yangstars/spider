# !/bin/env python
# -*- coding=utf-8 -*-
import requests
from PIL import Image
from json import loads
import cons
import json
import re
import datetime
from urllib import unquote
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import urllib3

urllib3.disable_warnings()
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# # 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import ssl

# 关闭12306的安全证书验证
ssl._create_default_https_context = ssl._create_unverified_context

station = {}
for i in cons.station_names.split('@'):
    if i:
        tmp = i.split('|')
        station[tmp[1]] = tmp[2]


class BuyTic(object):
    def __init__(self):
        # [*] 请输入验证码位置，以","分割[例如2,5]:4,6
        # self.userName = raw_input(u'[+] 用户名(用户名/邮箱/手机):')
        # self.pwd = raw_input(u'[+] 密码:')
        # self.realName = raw_input(u'[+] 请输入该账号用户的真实姓名:')
        # self.buyName = raw_input(u'[+] 请输入要订购车票的人的姓名：')
        # # self.pwd = getpass.getpass('[+] 密码:')
        # self.date = raw_input(u'[*] 请输入出行日期:(格式：2017-12-17)：')
        # self.from_station = station[raw_input(u'[*] 出发站：')]
        # self.to_station = station[raw_input(u'[*] 终点站：')]
        # self.train_number = raw_input(u'[*] 请输入车次号，以", "分割[例如G12,1237]:')
        self.userName = '951020602@qq.com'
        self.pwd = 'yangstars5038'
        self.realName = u'杨全帅'
        self.buyName = u'杨全帅'
        self.date = '2017-12-21'
        self.from_ = '北京'
        self.to_ = '上海'
        self.from_station = station[self.from_]
        self.to_station = station[self.to_]
        self.train_number = 'G7,G9'
        print  self.from_station, self.to_station,
        self.headers = {
            'Origin': 'https://kyfw.12306.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }

        self.cookies = {
            "_jc_save_fromDate": self.date,
            "_jc_save_fromStation": self.from_station,
            "_jc_save_toDate": self.date,
            "_jc_save_toStation": self.to_station,
            "_jc_save_wfdc_flag": "dc",
        }
        self.session = requests.session()
        # requests.utils.add_dict_to_cookiejar(self.session.cookies, self.cookies)
        # 创建一个网络请求session实现登录验证

    # 获取车站对应编码
    def getStationVal(self, stationName):
        station = {}
        for i in cons.station_names.split('@'):
            tmp = i.split('|')
            station[tmp[1]] = tmp[2]
            result = station[stationName]
            print result

    # 获取验证码图片
    def getImg(self):
        url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand";
        response = self.session.get(url=url, headers=self.headers, verify=False)
        # 把验证码图片保存到本地
        with open('img.jpg', 'wb') as f:
            f.write(response.content)
            # 用pillow模块打开并解析验证码,这里是假的，自动解析以后学会了再实现
        try:
            im = Image.open('img.jpg')
            # 展示验证码图片，会调用系统自带的图片浏览器打开图片，线程阻塞
            im.show()
            # 关闭，只是代码关闭，实际上图片浏览器没有关闭，但是终端已经可以进行交互了(结束阻塞)
            im.close()
        except:
            print u'[*] 请输入验证码'
            # =======================================================================
        captcha_solution = raw_input('[*] 请输入验证码位置，以","分割[例如2,5]:')
        return captcha_solution

        # 验证结果

    def checkYanZheng(self, solution):
        # 分割用户输入的验证码位置
        soList = solution.split(',')
        # 由于12306官方验证码是验证正确验证码的坐标范围,我们取每个验证码中点的坐标(大约值)
        yanSol = ['35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']
        yanList = []
        for item in soList:
            yanList.append(yanSol[int(item)])
            # 正确验证码的坐标拼接成字符串，作为网络请求时的参数
        yanStr = ','.join(yanList)
        checkUrl = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        data = {
            'login_site': 'E',  # 固定的
            'rand': 'sjrand',  # 固定的
            'answer': yanStr  # 验证码对应的坐标，两个为一组，跟选择顺序有关,有几个正确的，输入几个
        }
        # 发送验证
        cont = self.session.post(url=checkUrl, data=data, headers=self.headers, verify=False)
        # 返回json格式的字符串，用json模块解析
        dic = loads(cont.content)
        code = dic['result_code']
        # 取出验证结果，4：成功  5：验证失败  7：过期
        if str(code) == '4':
            return True
        else:
            return False

            # 发送登录请求的方法

    def loginTo(self):
        # 发送登录信息
        data = {
            "username": self.userName,
            "password": self.pwd,
            "appid": "otn"
        }
        url = "https://kyfw.12306.cn/passport/web/login"
        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            result = json.loads(response.text)
            print(result.get("result_message"), result.get("result_code"))
            if result.get("result_code") != 0:
                return False

        data = {"appid": "otn"}
        url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            result = json.loads(response.text)
            print(result.get("result_message"))
            newapptk = result.get("newapptk")

        data = {"tk": newapptk}
        url = "https://kyfw.12306.cn/otn/uamauthclient"
        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            result = json.loads(response.text)
            if result.get('result_code') != 0:
                return False

        url = "https://kyfw.12306.cn/otn/index/initMy12306"
        response = self.session.get(url, headers=self.headers)
        # print "------------------------------------------------------------"
        # print response.text
        # print "------------------------------------------------------------"
        if response.status_code == 200 and response.text.find(self.realName) != -1:
            print('[*] 恭喜你，登录成功，可以购票!')
            return True
        else:
            print '[*] 对不起，登录失败，请检查登录信息!'
            return False

    # 余票查询
    def getResidue(self):
        url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT" % (
            self.date, self.from_station, self.to_station)
        result = self.session.get(url=url, headers=self.headers, verify=False)
        json_html = json.loads(result.content)  # JSON编码的字符串转换回一个Python数据结构
        print "*************************************************************************"

        if json_html['data'] != None:
            flag = 0
            # while True:
            train_number = self.train_number.split(',')
            for i in json_html['data']['result']:
                # 对每一条数据进行判断，是否有票
                arrInfo = i.split('|')
                # print arrInfo
                if arrInfo[3] in train_number:
                    # 查看该车次是否有票（高铁 二等座：-6 == 有，一等座：-5  商务座：-4
                    if 'G' in arrInfo[3]:
                        if u'无' != arrInfo[-7]:
                            # 购票
                            print ('%s车次可购买二等座车票' % (str(arrInfo[3])))

                            # (5) 预订单data:
                            data = {
                                "secretStr": unquote(arrInfo[0]),
                                "train_date": self.date,
                                "back_train_date": self.date,
                                "tour_flag": "dc",
                                "purpose_codes": "ADULT",
                                "query_from_station_name": self.from_,
                                "query_to_station_name": self.to_,
                                "undefined": None
                            }
                            # print "data======++++++=%s" % (str(data))
                            # (6)检查用户是否存在 urlcheck = 'https://kyfw.12306.cn/otn/login/checkUser'
                            if self.checkUser():
                                # (7)提交预订单
                                if self.orderReserve(data):
                                    # (8)确认乘客信息
                                    print "获取用户信息"
                                    self.getUserInfo()

                        else:
                            print ('%s车次无二等座车票' % (str(arrInfo[3])))
                    elif 'D' in arrInfo[3]:  # 动车 二等座：-6
                        if u'无' != arrInfo[-7]:
                            # 购票
                            print ('%s车次可购买二等座车票' % (str(arrInfo[3])))
                        else:
                            print ('%s车次没有二等座车票' % (str(arrInfo[3])))
                    else:  # 硬座 和 硬卧 TODO
                        print arrInfo[-4]

    # 检查用户是否存在
    def checkUser(self):
        urlcheck = 'https://kyfw.12306.cn/otn/login/checkUser'
        checkData = {"_json_att": ""}
        checkRes = self.session.post(urlcheck, data=checkData, headers=self.headers, verify=False)
        # print checkRes.content
        json_check = json.loads(checkRes.content)  # JSON编码的字符串转换回一个Python数据结构
        if True == json_check['data']['flag']:
            print "[*] 预定购票用户校验成功！"
            return True

    # 订单预定
    def orderReserve(self, data):
        url_OrderRequest = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        res = self.session.post(url_OrderRequest, data=data, headers=self.headers)
        json_OrderRequest = json.loads(res.content)
        print '/////////////////////////////////////////////////////'
        print json_OrderRequest
        if json_OrderRequest['httpstatus'] == 200 and json_OrderRequest['status'] == True:
            return True

    # 获取用户信息
    def getUserInfo(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        response = self.session.get(url=url, headers=self.headers, verify=False)
        # print response.text
        # with open("foo.txt", "a+") as fo:
        #     fo.write(response.text);
        reg_REPEAT_SUBMIT_TOKEN = re.compile(r"globalRepeatSubmitToken = '(.*?)';")
        reg_key_check_isChange = re.compile(r"'key_check_isChange':'(.*?)'")
        reg_leftTicketStr = re.compile(r"'leftTicketStr':'(.*?)'")
        reg_purpose_codes = re.compile(r"'purpose_codes':'(.*?)'")
        reg_train_no = re.compile(r"'train_no':'(.*?)'")
        reg_train_location = re.compile(r"'train_location':'(.*?)'")
        reg_to_station_telecode = re.compile(r"'to_station_telecode':'(.*?)'")
        reg_from_station_telecode= re.compile(r"'from_station_telecode':'(.*?)'")
        reg_station_train_code= re.compile(r"'station_train_code':'(.*?)'")
        reg_ypInfoDetail= re.compile(r"'ypInfoDetail':'(.*?)'")


        items_REPEAT_SUBMIT_TOKEN  = re.findall(reg_REPEAT_SUBMIT_TOKEN, response.text)
        items_key_check_isChange = re.findall(reg_key_check_isChange, response.text)
        items_leftTicketStr = re.findall(reg_leftTicketStr, response.text)
        items_purpose_codes = re.findall(reg_purpose_codes, response.text)
        items_train_no = re.findall(reg_train_no, response.text)
        items_train_location = re.findall(reg_train_location, response.text)
        items_to_station_telecode = re.findall(reg_to_station_telecode, response.text)
        items_from_station_telecode = re.findall(reg_from_station_telecode, response.text)
        items_station_train_code = re.findall(reg_station_train_code, response.text)
        items_ypInfoDetail = re.findall(reg_ypInfoDetail, response.text)


        self.REPEAT_SUBMIT_TOKEN = items_REPEAT_SUBMIT_TOKEN[0]
        self.key_check_isChange =items_key_check_isChange[0]
        self.leftTicketStr = items_leftTicketStr[0]
        self.train_location = items_train_location[0]
        self.purpose_codes = items_purpose_codes[0]
        self.train_no = items_train_no[0]
        self.to_station_telecode = items_to_station_telecode[0]
        self.from_station_telecode = items_from_station_telecode[0]
        self.station_train_code = items_station_train_code[0]
        self.ypInfoDetail = items_ypInfoDetail[0]

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN
        }
        result = self.session.post(url=url, data=data, headers=self.headers, verify=False)
        dic = json.loads(result.content)
        for userinfo in dic['data']['normal_passengers']:
            if userinfo['passenger_name'] == self.buyName:
                print "下单"
                passengerTicketStr = "O,0," + userinfo['passenger_type'] + "," + userinfo['passenger_name'] + "," + userinfo['passenger_id_type_code'] + "," + userinfo['passenger_id_no'] + "," + userinfo['mobile_no'] + ",N"
                oldPassengerStr = userinfo['passenger_name']+ "," + userinfo['passenger_id_type_code'] + "," + userinfo['passenger_id_no'] + ",1_"

                data_checkOrder = {
                    'cancel_flag': '2',
                    'bed_level_order_num': '000000000000000000000000000000',
                    # 座位类型, 0, 票类型(成人 / 儿童), name, 身份类型(身份证 / 军官证….), 身份证, 电话号码, 保存状态
                    'passengerTicketStr':passengerTicketStr ,
                    'oldPassengerStr':oldPassengerStr,
                    'tour_flag': 'dc',
                    'whatsSelect':'1',
                    'randCode': '',
                    '_json_att': '',
                    'REPEAT_SUBMIT_TOKEN': str(self.REPEAT_SUBMIT_TOKEN)
                }

                data_ForQueue = {
                    'passengerTicketStr': passengerTicketStr,
                    'oldPassengerStr': oldPassengerStr,
                    'randCode': '',
                    'purpose_codes': str(self.purpose_codes),
                    'key_check_isChange': str(self.key_check_isChange),
                    'leftTicketStr': str(self.leftTicketStr),
                    'train_location': str(self.train_location),
                    'choose_seats': '',
                    'seatDetailType': '000',
                    'roomType': '00',
                    'dwAll': 'N',
                    '_json_att': '',
                    'REPEAT_SUBMIT_TOKEN': str(self.REPEAT_SUBMIT_TOKEN)
                }

                print "data_checkOrder=%s" % (data_checkOrder)
                print "data_ForQueue=%s" % (data_ForQueue)
                self.checkOrderInfo(data_checkOrder,data_ForQueue)

    # 验证订单
    def checkOrderInfo(self, data_checkOrder,data_ForQueue):

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        res = self.session.post(url=url,data=data_checkOrder,headers=self.headers, verify=False)
        json_checkOrder= json.loads(res.content)
        if json_checkOrder['data']['submitStatus'] == True:
            print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            # 获取队列个数
            url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
            GMT_FORMAT = '%a %b %d %Y 00:00:00 GMT+0800'
            # 生成datetime对象的过程和我可能不同，这里是拿当前时间来生成
            gmt_time = datetime.datetime.utcnow().strftime(GMT_FORMAT)
            data_getQueueCount = {
                'train_date': gmt_time,#Wed Dec 20 2017 00:00:00 GMT+0800
                'train_no': self.train_no,
                'stationTrainCode': self.station_train_code,
                'seatType': "O",#座位型号 二等座 O
                'fromStationTelecode': self.from_station_telecode,
                'toStationTelecoe': self.to_station_telecode,
                'leftTicket': self.ypInfoDetail,
                'purpose_codes': self.purpose_codes,
                'train_location': self.train_location,
                '_json_att': '',
                'REPEAT_SUBMIT_TOKEN':  self.REPEAT_SUBMIT_TOKEN
            }
            print data_getQueueCount
            res = self.session.post(url=url, data=data_getQueueCount, headers=self.headers, verify=False)
            with open("QueueCount.txt", "a+") as fo:
                fo.write(res.text)

            url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
            res = self.session.post(url, data=data_ForQueue,headers=self.headers, verify=False)
            with open("ForQueue.txt", "a+") as fo:
                fo.write(res.text)

            print "下单成功"


if __name__ == '__main__':

    buyTic = BuyTic()
    # （1）图片验证
    yan = buyTic.getImg()
    chek = False
    # 只有验证成功后才能执行登录操作
    while not chek:
        chek = buyTic.checkYanZheng(yan)
        if chek:
            print '[*] 验证通过!'
            # （2）登陆
            if buyTic.loginTo():
                # （3）登陆成功，余票查询
                buyTic.getResidue()
                # (4)检查用户是否存在
                # if buyTic.checkUser():
                #    continue

        else:
            print '[*] 验证失败，请重新验证!'
