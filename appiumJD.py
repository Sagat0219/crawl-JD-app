#coding=utf-8
from appium import webdriver
from selenium.webdriver.common.by import By #支持的定位器分类
from selenium.webdriver.support.ui import WebDriverWait #动态等待页面上元素出现
from selenium.webdriver.support import expected_conditions as EC    #期望条件
from selenium.common.exceptions import NoSuchElementException   #处理找不到元素时的异常
from time import sleep

#要搜索的商品list
keywords = ['ipad','保温杯','iphone xs','榨汁机']

class Action():
    def __init__(self):
        # 驱动配置
        self.desired_caps = {
            'platformName': 'Android',  #系统说明
            'deviceName': 'MI_6_',  #手机名
            'appPackage': 'com.jingdong.app.mall',  #app包名
            'appActivity': 'com.jingdong.app.mall.main.MainActivity',   #启动入口
            'unicodeKeyboard':True  #
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.wait = WebDriverWait(self.driver, 30)

    def homepage(self):
        #同意协议
        agree = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jingdong.app.mall:id/bu5')))
        agree.click()
        sleep(6)

        #如果有弹出注册广告页，关闭它
        try:
            self.driver.find_element_by_accessibility_id("注册领取 Link")
            self.driver.tap([(679,75)])
        except NoSuchElementException:
            pass

    def search(self):
        for keyword in keywords:
            # 点击进入搜索页面
            search = self.wait.until(EC.presence_of_element_located((By.ID,'com.jingdong.app.mall:id/rd')))
            search.click()
            # 输入搜索文本
            box = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.search:id/search_text')))
            box.set_text(keyword)
            # 点击搜索按钮
            button = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jingdong.app.mall:id/awr')))
            button.click()
            # 选择第一个卖家店，点击进入商品详情
            xpath = '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]'
            view = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            view.click()
            sleep(5)

            # 找到'查看全部评价'按钮，进入评价详情
            found = False
            while not found:
                self.driver.swipe(300, 600, 300, 300)
                try:
                    self.driver.find_element_by_id('com.jd.lib.productdetail:id/pd_comment_left_btn')
                    found = True
                except NoSuchElementException:
                    sleep(0.5)
            allcomments = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.productdetail:id/pd_comment_left_btn')))
            allcomments.click()
            sleep(3)

            #向上滑动获取评价数据
            self.scroll()

            #回到首页，准备搜索下一件商品
            more = self.driver.find_element_by_id('com.jd.lib.productdetail:id/pd_nav_more')
            more.click()
            self.driver.tap([(600, 215)])


    #向上滑动获取评价数据
    def scroll(self):
        i=0
        while i<11:
            # 模拟拖动
            self.driver.swipe(300, 1000, 300, 100)
            sleep(2)
            i += 1

if __name__ == '__main__':
    action = Action()
    action.homepage()
    action.search()
    action.driver.quit()