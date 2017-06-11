# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import re
# from pyquery import PyQuery as pq
# from config import *
# import pymongo

# client=pymongo.MongoClient(MOGODB_URL)
# db=client[MOGODB_DB]

# path = "C:/Users/zhangp/AppData/Local/Google/Chrome/Application/chromedriver.exe"
# browser = webdriver.Chrome(executable_path=path)   #环境变量没有添加成功，每次启动的时候自己寻找环境变量


# wait = WebDriverWait(browser, 10)

# def search():
#     try:
#         browser.get('https://www.taobao.com')
#         input = wait.until(
#              EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
#             )                 #查找淘宝输入框
#         submit = wait.until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))  #寻找淘宝搜索按钮
#         input.send_keys('美食')   #输入搜索关键字
#         submit.click()   #提交按钮
#         total=wait.until(
#              EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
#             )                 #查找美食全部多少页是否加载出来了
#         get_products()
#         return total.text  #加载出一共多少页
#     except TimeoutException:
#         return search()

# def next_page(num_page):
#     try:
#         input = wait.until(
#              EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
#             )                
#         submit = wait.until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))  
#         input.clear()
#         input.send_keys(num_page)   
#         submit.click()   #提交按钮
#         wait.until(
#              EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(num_page))
#             )
#         get_products()      
#     except TimeoutException:
#         return next_page(num_page)

# def get_products():
#     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))  #判断整个美食界面是否加载出来了
#     html = browser.page_source 
#     doc = pq(html)  #解析一下界面
#     items = doc('#mainsrp-itemlist .items .item').items()  #得到整个匹配的单项
#     for item in items:
#         product = {
#             'image': item.find('.pic .img').attr('src'),
#             'price': item.find('.price').text(),
#             'deal': item.find('.deal-cnt').text()[:-3],
#             'title': item.find('.title').text(),
#             'shop': item.find('.shop').text(),
#             'location': item.find('.location').text()
#         }
#         print(product)
#         save_mogodb(product)

# def save_mogodb(product):
# 	try:
# 		db[MOGODB_TABLE].insert(product)
# 		print("保存到数据库成功",product)
# 	except Exception:
# 		print("保存到数据库出错！",product)

# def main():
#     total=search()
#     pattern=re.compile(r'(\d+)',re.S)
#     total=int(re.search(pattern,total).group(1))
#     for i in range(2,total+1):
#         next_page(i)

#     browser.close()

# if __name__=="__main__":
#     main()

#上面的版本是调用Chrome浏览器的版本

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pyquery import PyQuery as pq
from config import *
import pymongo

client=pymongo.MongoClient(MOGODB_URL)
db=client[MOGODB_DB]

path = "C:/Users/zhangp/Desktop/用到的一些配置文件/phantomjs-2.1.1-windows/bin/phantomjs.exe"
browser = webdriver.PhantomJS(executable_path=path,service_args=SERVICE_ARGS)


wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)  #给PhantomJS浏览器一个默认的大小，否则会出错

def search():
    print('正在搜索')
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
             EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
            )                 #查找淘宝输入框
        submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))  #寻找淘宝搜索按钮
        input.send_keys(KEYWORD)   #输入搜索关键字
        submit.click()   #提交按钮
        total=wait.until(
             EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
            )                 #查找美食全部多少页是否加载出来了
        get_products()
        return total.text  #加载出一共多少页
    except TimeoutException:
        return search()

def next_page(num_page):
    print('正在翻页',num_page)
    try:
        input = wait.until(
             EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
            )                
        submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))  
        input.clear()
        input.send_keys(num_page)   
        submit.click()   #提交按钮
        wait.until(
             EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(num_page))
            )
        get_products()      
    except TimeoutException:
        next_page(num_page)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))  #判断整个美食界面是否加载出来了
    html = browser.page_source 
    doc = pq(html)  #解析一下界面
    items = doc('#mainsrp-itemlist .items .item').items()  #得到整个匹配的单项
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_mogodb(product)

def save_mogodb(product):
    try:
        db[MOGODB_TABLE].insert(product)
        print("保存到MONGODB数据库成功",product)
    except Exception:
        print("保存到MONGODB数据库出错！",product)

def main():
    try:
        total=search()
        pattern=re.compile(r'(\d+)',re.S)
        total=int(re.search(pattern,total).group(1))
        for i in range(2,total+1):
            next_page(i)
    except Exception:
        print('出错啦')
    finally:
        browser.close()

if __name__=="__main__":
    main()