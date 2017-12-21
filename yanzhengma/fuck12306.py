#-*- coding:utf-8 -*-sss

from PIL import Image
from PIL import ImageFilter
import urllib
import urllib2
import requests
import re
import json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# if hasattr(ssl, '_create_unverified_context'):
#     ssl._create_default_https_context = ssl._create_unverified_context


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"

pic_url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.7174227166135074"

def get_img():
    resp = urllib.urlopen(pic_url)
    raw = resp.read()
    f = open("F:/python/workspace/spider/yanzhengma/screenshots/" + str(1) + ".jpg", 'wb')
    # with open("./screenshots/tmp.jpg", 'wb') as fp:
    #     fp.write(raw)
    f.write(raw)
    f.close()
    print 1111
    return Image.open("./screenshots/tmp.jpg")


def getImg():
    url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand";
    response = urllib.urlopen(url=pic_url,)
    # 把验证码图片保存到本地
    with open('../screenshots/img.jpg', 'wb') as f:
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

def get_sub_img(im, x, y):
    assert 0 <= x <= 3
    assert 0 <= y <= 2
    WITH = HEIGHT = 68
    left = 5 + (67 + 5) * x
    top = 41 + (67 + 5) * y
    right = left + 67
    bottom = top + 67

    return im.crop((left, top, right, bottom))



def baidu_image_upload(im):
    url = "http://image.baidu.com/pictureup/uploadshitu?fr=flash&fm=index&pos=upload"

    im.save("./query_temp_img.png")
    raw = open("./query_temp_img.png", 'rb').read()

    files = {
        'fileheight'   : "0",
        'newfilesize'  : str(len(raw)),
        'compresstime' : "0",
        'Filename'     : "image.png",
        'filewidth'    : "0",
        'filesize'     : str(len(raw)),
        'filetype'     : 'image/png',
        'Upload'       : "Submit Query",
        'filedata'     : ("image.png", raw)
    }

    resp = requests.post(url, files=files, headers={'User-Agent':UA})

    #  resp.url
    redirect_url = "http://image.baidu.com" + resp.text
    return redirect_url



def baidu_stu_lookup(im):
    redirect_url = baidu_image_upload(im)

    #print redirect_url
    resp = requests.get(redirect_url)

    html = resp.text

    return baidu_stu_html_extract(html)


def baidu_stu_html_extract(html):
    pattern = re.compile(r"'multitags':\s*'(.*?)'")
    matches = pattern.findall(html)
    if not matches:
        return '[ERROR?]'

    tags_str = matches[0]

    result =  list(filter(None, tags_str.replace('\t', ' ').split()))

    return '|'.join(result) if result else '[UNKOWN]'


def ocr_question_extract(im):
    # git@github.com:madmaze/pytesseract.git
    global pytesseract
    try:
        import pytesseract
    except:
        print "[ERROR] pytesseract not installed"
        return
    im = im.crop((127, 3, 260, 22))
    im = pre_ocr_processing(im)
    # im.show()
    return pytesseract.image_to_string(im, lang='chi_sim').strip()


def pre_ocr_processing(im):
    im = im.convert("RGB")
    width, height = im.size

    white = im.filter(ImageFilter.BLUR).filter(ImageFilter.MaxFilter(23))
    grey = im.convert('L')
    impix = im.load()
    whitepix = white.load()
    greypix = grey.load()

    for y in range(height):
        for x in range(width):
            greypix[x,y] = min(255, max(255 + impix[x,y][0] - whitepix[x,y][0],
                                        255 + impix[x,y][1] - whitepix[x,y][1],
                                        255 + impix[x,y][2] - whitepix[x,y][2]))

    new_im = grey.copy()
    binarize(new_im, 150)
    return new_im


def binarize(im, thresh=120):
    assert 0 < thresh < 255
    assert im.mode == 'L'
    w, h = im.size
    for y in xrange(0, h):
        for x in xrange(0, w):
            if im.getpixel((x,y)) < thresh:
                im.putpixel((x,y), 0)
            else:
                im.putpixel((x,y), 255)


if __name__ == '__main__':
    im = getImg()
    #im = Image.open("./tmp.jpg")
    try:
        print 'OCR Question:', ocr_question_extract(im)
    except Exception as e:
        print '<OCR failed>', e
    for y in range(2):
        for x in range(4):
            im2 = get_sub_img(im, x, y)

            result = baidu_stu_lookup(im2)
            print (y,x), result
