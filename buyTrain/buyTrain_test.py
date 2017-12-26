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
import time
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib3
import ssl

urllib3.disable_warnings()
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# # 禁用安全请求警告
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 关闭12306的安全证书验证
ssl._create_default_https_context = ssl._create_unverified_context

#获取车站编码
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
        # self.seatType = raw_input(u'[*] 请输入座位席别，以", "分割[例如二等座,一等座，硬座，硬卧]:')
        # self.lianzhong_username = raw_input(u'[*] 请输入联众账号:')
        # self.lianzhong_password = raw_input(u'[*] 请输入联众密码:')

        self.userName = '951020602@qq.com'
        self.pwd = 'yangstars5038'
        # self.realName = u'杨全帅'
        self.buyName = u'杨全帅'
        self.date = '2017-12-26'
        self.from_ = '枣庄'
        self.to_ = '上海'
        self.train_number = 'K47'
        self.lianzhong_username = 'moxiao'
        self.lianzhong_password = 'moxiao1990,.'

        self.seatType='1'#O:二等座  1：硬座  2 软卧是4  硬卧 3
        self.from_station = station[self.from_]
        self.to_station = station[self.to_]

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
            # print result

    # 获取验证码图片
    def getImg(self):
        url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand";
        response = self.session.get(url=url, headers=self.headers, verify=False)
        # 把验证码图片保存到本地
        file_name = 'F:/python/workspace/spider/buyTrain/tupian.png'
        with open(file_name, 'wb') as f:
            f.write(response.content)

        response = self.lianzhong(file_name)
        dic = loads(response.content)
        # print "dic=%s"%(dic)
        if dic['result']== True :
            yanList = []
            zuobiao= str(dic['data']['val'])
            if zuobiao.count('|') > 0:
                return str(zuobiao.replace('|', ','))
            else:
                return zuobiao
            print "[*]获取验证码坐标成功！"
        else:
            print "[*]获取验证码坐标失败！"
            return

    def lianzhong(self,file_name):
        '''
                main() 参数介绍
                api_username    （API账号）             --必须提供
                api_password    （API账号密码）         --必须提供
                file_name       （需要打码的图片路径）   --必须提供
                api_post_url    （API接口地址）         --必须提供
                yzm_min         （验证码最小值）        --可空提供
                yzm_max         （验证码最大值）        --可空提供
                yzm_type        （验证码类型）          --可空提供
                tools_token     （工具或软件token）     --可空提供
        '''
        url_lianzhong = 'http://v1-http-api.jsdama.com/api.php?mod=php&act=upload'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Connection': 'keep-alive',
            'Host': 'v1-http-api.jsdama.com',
            'Upgrade-Insecure-Requests': '1'
        }
        files = {
            'upload': (file_name, open(file_name, 'rb'), 'image/png')
        }
        data = {
            'user_name': 'moxiao',
            'user_pw': 'moxiao1990,.',
            'yzm_minlen': '1',
            'yzm_maxlen': '8',
            'yzmtype_mark': '1303',
            'zztool_token': ''
        }
        s = requests.session()
        # r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False, proxies=proxies)
        res = s.post(url_lianzhong, headers=headers, data=data, files=files, verify=False)
        # print(res.text)
        return res

        # 验证结果

    def checkYanZheng(self, solution):
        # 分割用户输入的验证码位置
        # print "solution=%s"%(solution)
        checkUrl = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        data = {
            'login_site': 'E',  # 固定的
            'rand': 'sjrand',  # 固定的
            'answer': solution  # 验证码对应的坐标，两个为一组，跟选择顺序有关,有几个正确的，输入几个
        }

        # print data
        # 发送验证
        cont = self.session.post(url=checkUrl, data=data, headers=self.headers, verify=False)
        # 返回json格式的字符串，用json模块解析
        dic = loads(cont.content)
        code = dic['result_code']
        # 取出验证结果，4：成功  5：验证失败  7：过期
        if str(code) == '4':
            print '[*] 图片验证通过!'
            return True
        else:
            print '<!> 图片验证失败，请重新验证!'
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
            # print(result.get("result_message"), result.get("result_code"))
            if result.get("result_code") != 0:
                return False

        data = {"appid": "otn"}
        url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 200:
            result = json.loads(response.text)
            # print(result.get("result_message"))
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
        # if response.status_code == 200 and response.text.find(self.realName) != -1:
        if response.status_code == 200 :
            print('[*] 恭喜你，登录成功，可以购票!')
            return True
        else:
            print '<!> 对不起，登录失败，请检查登录信息!'
            return False

    # 余票查询
    def getResidue(self):
        url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT" % (
            self.date, self.from_station, self.to_station)
        result = self.session.get(url=url, headers=self.headers, verify=False)
        json_html = json.loads(result.content)  # JSON编码的字符串转换回一个Python数据结构
        if json_html['data'] != None:
            flag = 0
            # while True:
            train_number = self.train_number.split(',')# 你想购票的车次号 如 G7,G9
            for train_data in json_html['data']['result']:
                # 对每一条数据进行判断，是否有票
                arrInfo = train_data.split('|')#每一班车次的所有信息
                # print "-------------------------------------------------"
                # print arrInfo
                # print "-------------------------------------------------"
                if arrInfo[3] in train_number:#只需要抓取你定义的车次信息
                    # 查看该车次是否有票（高铁 二等座：-7 （30） 有，一等座：-6（31）  商务座：-5（32）  硬座：29 软卧：23  硬卧：28  无座：26
                    # (5) 预订单data:
                    data_orderReserve = {
                        "secretStr": unquote(arrInfo[0]),
                        "train_date": self.date,
                        "back_train_date": self.date,
                        "tour_flag": "dc",
                        "purpose_codes": "ADULT",
                        "query_from_station_name": self.from_,
                        "query_to_station_name": self.to_,
                        "undefined": None
                    }
                    #高铁
                    if u'无' != arrInfo[-7] and arrInfo[-7] != "" :#说明是高铁 二等座
                        print ('[*]可购买%s车次 二等座 车票' % (str(arrInfo[3])))
                        return  data_orderReserve
                        # # (6)检查用户是否存在 urlcheck = 'https://kyfw.12306.cn/otn/login/checkUser'
                        # if self.checkUser():
                        #     # (7)提交预订单
                        #     if self.orderReserve(data):
                        #         # (8)确认乘客信息
                        #         #print "[*]获取用户信息"
                        #         self.getUserInfo()
                    elif u'无' != arrInfo[28] and arrInfo[28] != "":
                        print ('[*]可购买%s车次 硬卧 车票' % (str(arrInfo[3])))
                        return data_orderReserve
                    elif u'无' != arrInfo[29] and arrInfo[29] != "":
                        print ('[*]可购买%s车次 硬座 车票' % (str(arrInfo[3])))
                        return data_orderReserve
                    elif u'无' != arrInfo[26] and arrInfo[26] != "":
                        print ('[*]可购买%s车次 无座 车票' % (str(arrInfo[3])))
                        return data_orderReserve
                    else:
                        print ('<!> %s车次无票' % (str(arrInfo[3])))
                        return False

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
    def orderReserve(self, data_orderReserve):
        url_OrderRequest = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        res = self.session.post(url_OrderRequest, data=data_orderReserve, headers=self.headers)
        json_OrderRequest = json.loads(res.content)
        # print json_OrderRequest
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
                print "[*]下单处理中···"
                passengerTicketStr = self.seatType +",0," + userinfo['passenger_type'] + "," + userinfo['passenger_name'] + "," + userinfo['passenger_id_type_code'] + "," + userinfo['passenger_id_no'] + "," + userinfo['mobile_no'] + ",N"
                oldPassengerStr = userinfo['passenger_name']+ "," + userinfo['passenger_id_type_code'] + "," + userinfo['passenger_id_no'] + ",1_"

                data_checkOrder = {
                    'cancel_flag': '2',
                    'bed_level_order_num': '000000000000000000000000000000',
                    # 座位类型, 0, 票类型(成人 / 儿童), name, 身份类型(身份证 / 军官证….), 身份证, 电话号码, 保存状态
                    'passengerTicketStr':passengerTicketStr ,
                    'oldPassengerStr':oldPassengerStr,
                    'tour_flag': 'dc',
                    # 'whatsSelect':'1',
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
                # print "data_checkOrder=%s" % (data_checkOrder)
                # print "data_ForQueue=%s" % (data_ForQueue)
                return self.checkOrderInfo(data_checkOrder,data_ForQueue)


    # 验证订单
    def checkOrderInfo(self, data_checkOrder,data_ForQueue):
        print "[*]校验订单中······"
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        res = self.session.post(url=url,data=data_checkOrder,headers=self.headers, verify=False)
        json_checkOrder= json.loads(res.content)
        # print "json_checkOrder=%s"%(json_checkOrder)
        if json_checkOrder['data']['submitStatus'] == True:
            # 获取队列个数
            url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
            GMT_FORMAT = '%a %b %d %Y 00:00:00 GMT+0800'
            # 生成datetime对象的过程和我可能不同，这里是拿当前时间来生成
            gmt_time = datetime.datetime.utcnow().strftime(GMT_FORMAT)
            data_getQueueCount = {
                'train_date': gmt_time,#Wed Dec 20 2017 00:00:00 GMT+0800
                'train_no': self.train_no,
                'stationTrainCode': self.station_train_code,
                'seatType': self.seatType,#座位型号 二等座 O
                'fromStationTelecode': self.from_station_telecode,
                'toStationTelecoe': self.to_station_telecode,
                'leftTicket': self.ypInfoDetail,
                'purpose_codes': self.purpose_codes,
                'train_location': self.train_location,
                '_json_att': '',
                'REPEAT_SUBMIT_TOKEN':  self.REPEAT_SUBMIT_TOKEN
            }
            # print "data_getQueueCount=%s" % (data_getQueueCount)
            res = self.session.post(url=url, data=data_getQueueCount, headers=self.headers, verify=False)
            # with open("QueueCount.txt", "a+") as fo:
            #     fo.write(res.text)
            url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
            res = self.session.post(url, data=data_ForQueue,headers=self.headers, verify=False)
            # with open("ForQueue.txt", "a+") as fo:
            #     fo.write(res.text)
            json_checkOrder = json.loads(res.content)
            if json_checkOrder['data']['submitStatus'] == True :
                print "[*]下单提交成功，请登陆网站进行支付！"
                return True
                #发送手机短信
            else :
                print "<!>下单提交成功，请登陆网站进行支付！"
                return  False




#程序入口
if __name__ == '__main__':
    buyTic = BuyTic()
    # （1）图片验证
    yan = buyTic.getImg()
    chek = False
    # 只有验证成功后才能执行登录操作
    while not chek:
        chek = buyTic.checkYanZheng(yan)
        if chek:
            # （2）登陆
            if buyTic.loginTo():
                #循环
                while(True):
                    # （3）登陆成功，余票查询
                    data_orderReserve = buyTic.getResidue()
                    if data_orderReserve != False:
                        # (4)检查用户是否存在 urlcheck = 'https://kyfw.12306.cn/otn/login/checkUser'
                        if buyTic.checkUser():
                            # (7)提交预订单
                            if buyTic.orderReserve(data_orderReserve):
                                # (8)确认乘客信息
                                 if buyTic.getUserInfo()== True :
                                    break
                                 else:
                                     time.sleep(10)
