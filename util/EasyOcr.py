# -*- coding:utf-8 -*-
from http import cookiejar

import easyocr
from PIL import Image
import time
import datetime
from PIL import Image
import easyocr
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import cv2
import urllib
import os
import numpy as np
import copy
from io import StringIO
import requests
from urllib import request

''' 根据该像素周围点为黑色的像素数（包括本身）来判断是否把它归属于噪声，如果是噪声就将其变为白色'''
'''
	input:  img:二值化图
			number：周围像素数为黑色的小于number个，就算为噪声，并将其去掉，如number=6，
			就是一个像素周围9个点（包括本身）中小于6个的就将这个像素归为噪声
	output：返回去噪声的图像
'''

def del_noise(img,number):
    height = img.shape[0]
    width = img.shape[1]

    img_new = copy.deepcopy(img)
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            point = [[], [], []]
            count = 0
            point[0].append(img[i - 1][j - 1])
            point[0].append(img[i - 1][j])
            point[0].append(img[i - 1][j + 1])
            point[1].append(img[i][j - 1])
            point[1].append(img[i][j])
            point[1].append(img[i][j + 1])
            point[2].append(img[i + 1][j - 1])
            point[2].append(img[i + 1][j])
            point[2].append(img[i + 1][j + 1])
            for k in range(3):
                for z in range(3):
                    if point[k][z] == 0:
                        count += 1
            if count <= number:
                img_new[i, j] = 255
    return img_new


if __name__=='__main__':
    reader = easyocr.Reader(['ch_sim', 'en'])
    driver = webdriver.Chrome()
    driver.get('http://test.com')
    # 此处的open方法打开网页
    cookies = driver.get_cookies()
    # 打印cookie信息
    arr = ('test1','test2')
    time.sleep(3)  # 强制等待3秒再执行下一步
    driver.find_element_by_id("username").send_keys('username')
    driver.find_element_by_id("password").send_keys('pwd')
    rd=driver.find_element_by_id("captchaid")
    url = "http://test.com"
    data = requests.get(url)
    soup = BeautifulSoup(data, 'lxml')
    captchaId = soup.find('img', attrs={'id': 'captchaid'})['src'].split('?')[1].split('&')[0].split('=')[1]
    print("captchaId="+captchaId)

    for item in cookies:
        print('Value = %s' % item['value'])
    #driver.save_screenshot("C:/Users/musaxi/Desktop/1/captchaid.jpg")
    img_dir = 'C:/Users/musaxi/Desktop/1'
    img_name = os.listdir(img_dir)  # 列出文件夹下所有的目录与文件
    kernel = np.ones((5, 5), np.uint8)
    for i in range(len(img_name)):
        path = os.path.join(img_dir, img_name[i])
        image = cv2.imread(path)
        name_list = list(img_name[i])[:6]
        name = ''.join(name_list)
            # 灰度化
            # print(image.shape)
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # 二值化
        result = cv2.adaptiveThreshold(grayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
            # 去噪声
        img = del_noise(result, 6)
        img = del_noise(img, 4)
        img = del_noise(img, 3)
            # 加滤波去噪
        im_temp = cv2.bilateralFilter(src=img, d=15, sigmaColor=130, sigmaSpace=150)
        im_temp = im_temp[1:-1,1:-1]
        im_temp = cv2.copyMakeBorder(im_temp, 83, 83, 13, 13, cv2.BORDER_CONSTANT, value=[255])
        cv2.imwrite('C:/Users/musaxi/Desktop/1/%s.jpg' %(name), im_temp)
        captchaid_val = reader.readtext(r'C:/Users/musaxi/Desktop/1/%s.jpg' %(name),detail=0)
        print(captchaid_val)
    driver.find_element_by_id("captchaid").send_keys(captchaid_val)
    driver.find_element_by_name("submit1").submit()

    flag = True
    def isElementExist(driver, param):
        flag = True
        browser = driver
        try:
            browser.find_element_by_xpath(param)
            return flag
        except:
            flag = False
            return flag
    for tp in arr:
        driver.find_element_by_id("email_serach").send_keys(tp)
        driver.find_element_by_id("search_link").click()  # 页面加载完就执行
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "load-simple-dialog")))
            if isElementExist(driver, "//*[@id='load-simple-dialog']/table/tbody[2]/tr[2]/td[2]"):
                value1 = driver.find_element_by_xpath("//*[@id='load-simple-dialog']/table/tbody[2]/tr[2]/td[2]").text
                value2 = driver.find_element_by_xpath("//*[@id='load-simple-dialog']/table/tbody[2]/tr[2]/td[3]").text
                value3 = driver.find_element_by_xpath("//*[@id='load-simple-dialog']/table/tbody[2]/tr[2]/td[4]").text
                value4 = driver.find_element_by_xpath("//*[@id='load-simple-dialog']/table/tbody[2]/tr[2]/td[5]").text
                value5 = driver.find_element_by_xpath("//*[@id='load-simple-dialog']/table/tbody[2]/tr[2]/td[6]").text
                value6 = driver.find_element_by_xpath("//*[@id='load-simple-dialog']/table/tbody[2]/tr[2]/td[7]").text
                print(value1 + "," + value2 + "," + value3 + "," + value4 + "," + value5 + "," + value6)

            elif isElementExist(driver, "//*[@id='load-simple-dialog']/table/tbody/tr[2]/td[1]/a"):
                print(tp + " 有重名！")
            else:
                print(tp + " 员工没找到！")
        finally:
            driver.find_element_by_xpath("/html/body/div[2]/div[1]/a").click()
            flag = False
        if flag:
            driver.find_element_by_xpath("/html/body/div[2]/div[1]/a").click()
            flag = True
        driver.find_element_by_id("email_serach").clear()  # 清空数据

