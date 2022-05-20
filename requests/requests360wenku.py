import requests
import time
import os
import img2pdf
from selenium import webdriver
from selenium.webdriver.common.by import By

def drop_down(driver):
    #执行滚轮的操作 
    for x in range(1,18,2):
        time.sleep(1)
        j = x/18 # 1/9 3/9 5/9 9/9
        #document.documentElement.scrollTop 指定滚轮条的位置
        #document.documentElement.scrollHeight 获取浏览器页面最大高度
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)
        
def download_360wenku(driver = None, url = '', headers = {}):
    ''' 
    自动化测试并且爬取网站内容,
    这里针对360文库的图片文件进行爬取.
    '''
    if not driver:
        driver = webdriver.Firefox()
    driver.get(url)
    try :
        continue_web = driver.find_element(by=By.XPATH,value='/html/body/div[4]/div[2]/div[1]/div[5]/div[2]/a')
        driver.execute_script("$(arguments[0]).click()", continue_web)
        url+= '##continue'
    except:
        print("无需加载资源")
    drop_down(driver)
    img_first = driver.find_element(by=By.XPATH,value='//*[@id="js-cont-first"]/img')
    img_li = driver.find_elements(by=By.XPATH,value='//*[@id="js-cont"]/div/img')
    img_li.insert(0,img_first)
    print("获取到src资源有：",len(img_li))
    img_li = list(map(lambda img:img.get_attribute('src') , img_li))
    try:
        os.mkdir('image')
    except:
        print("image目录已经存在无需创建")
    for i in range(len(img_li)):
        img_url = img_li[i]
        img_content = requests.get(img_url,headers).content
        with open(f'image\{i}.png','wb') as f:
            f.write(img_content)
    driver.quit()
    return None

def imgtopdf():
    '''
    对当前目录下的image文件内的所有图片进行打包,
    并且创建并写入一个pdf文件中以便阅读.
    '''
    try:
        os.remove('a.pdf')
    except:
        print("文件pdf不存在，可以直接创建pdf")
    with open("a.pdf","wb") as f:
        #以二进制写入的方式打开文件f
        ls = ["image/" + img_name for img_name in os.listdir("image")]
        #读取image文件下的所有图片路径,调用os模块listdir方法获取image下所有文件名
        #对所有文件名前加上image/作为路径名，返回给列表ls
        ls.sort(key = lambda x:int(x.split('/')[1].split('.')[0]))
        #通过sort函数排序，这里的key的值为：
        #lambda函数隐式调用x的方法，对所有x以其分割后处于/与.之间的整型数大小作为排序的依据
        f.write(img2pdf.convert(ls))
        #整理好的ls列表交给img2pdf模块去写入文件,按照排序顺序将爬取到的图片整理成pdf格式文件
    return None

def clear():
    '''
    清理模块,对image目录下的文件进行清理.
    '''
    for i in [img_name for img_name in os.listdir('image')]:
        os.remove(f'image\{i}')
    return None

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 SLBrowser/7.0.0.12151 SLBChan/30'
    }
#请求头，这里的user-agent自己写，这里就用我自己电脑上的了，360文档似乎对爬虫挺友好的，就这一个参数就够了
url = "https://wenku.so.com/d/42e93894486f5d7929cbf0a0a6e35762"
#测试url:https://wenku.so.com/d/42e93894486f5d7929cbf0a0a6e35762
#测试url：https://wenku.so.com/d/ff3e236cc5efbf8d4bfbb2211f29a847
#测试url:https://wenku.so.com/d/dff6f4a81a842c367dba75a45d3afafd
driver = webdriver.Firefox()
download_360wenku(driver, url, headers)
imgtopdf()
clear()

