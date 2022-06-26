import datetime
import os
import uuid
import re
import cv2
from PIL import Image, ImageEnhance
import pytesseract
import time

path = r"C:\Users\musaxi\Desktop\照片"


#path = r"C:\Users\musaxi\Desktop\新建文件夹"



#img = img.convert('L')  # 转成灰度
#enh_con = ImageEnhance.Contrast(img)
#contrast = 5.5
#img = enh_con.enhance(contrast)
#img.show()
#text = pytesseract.image_to_string(img, lang='chi_sim')
#print(text)


def read_directory(directory_name):
    i = 0
    j = 0
    flag = True  # 用于判断成功、失败+1
    newName = ""
    regex_str = "(^.*?[姓].*?[名].*?)"
    print("耗时=" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    for filename in os.listdir(directory_name):
        reFlag = True  # 用于判断有重复数据，就不在答应成功、失败数据
        img = Image.open(directory_name + "/" + filename)
        text = pytesseract.image_to_string(img, lang='chi_sim')
        match_obj = re.match(regex_str, text.replace("\n",""))
        if (match_obj == None):
            img = img.convert('L')  # 转成灰度
            text = pytesseract.image_to_string(img, lang='chi_sim')
            match_obj = re.match(regex_str, text.replace("\n",""))
        if (match_obj == None):
            img_db = Image.open(directory_name + "/" + filename)
            enh_con = ImageEnhance.Contrast(img_db)  # 增强对比度
            contrast = 5.5
            img_db = enh_con.enhance(contrast)
            text = pytesseract.image_to_string(img_db, lang='chi_sim')
            match_obj = re.match(regex_str, text.replace("\n",""))
        if (match_obj == None):
            img_dbhd = Image.open(directory_name + "/" + filename)  # 灰度+对比度
            img_dbhd = img_dbhd.convert("L")
            enh_con = ImageEnhance.Contrast(img_dbhd)  # 增强对比度
            contrast = 5.5
            img_dbhd = enh_con.enhance(contrast)
            text = pytesseract.image_to_string(img_dbhd, lang='chi_sim')
        textarr = text.split("\n")
        k = 0  # 用于取数组值
        for strTp in textarr:
            k = k + 1
            strTemp = strTp.replace(" ", "")
            filenameTp = filename[filename.find("."):len(filename)]
            if strTemp.find("姓名") >= 0:
                if strTemp[3:len(strTemp)] == "":  # 判断姓名:姓名
                    newName = "无法识别" + str(uuid.uuid1())
                    flag = False
                # 判断姓名不在同一行，识别在第18个数字。
                if strTemp[3:len(strTemp)] == "" and textarr[k].replace(" ", "").find("身份") >= 0:
                    try:
                        if len(textarr[18].replace(" ", "")) > 4:
                            tpName = textarr[k + 3].replace(" ", "")
                        else:
                            tpName = textarr[18].replace(" ", "")
                        os.rename(directory_name + "/" + filename,
                                  directory_name + "/" + tpName + filenameTp)
                        flag = True
                        newName = tpName
                        break
                    except FileExistsError as e:
                        uuidName = "_" + str(uuid.uuid1())
                        os.rename(directory_name + "/" + filename,
                                  directory_name + "/" + newName + uuidName + filenameTp)
                        newName = "有重复！"
                        flag = True
                        break
                    break  # 识别成功就不在判断后续值
                else:
                    newName = strTemp[3:len(strTemp)]
                try:
                    newName = newName.replace(":", "")
                    os.rename(directory_name + "/" + filename,
                              directory_name + "/" + newName + filenameTp)
                    flag = True
                    break
                except FileExistsError as e:
                    # 有重复的改成重复—+uuid
                    uuidName = "_" + str(uuid.uuid1())
                    os.rename(directory_name + "/" + filename,
                              directory_name + "/" + newName + uuidName + filenameTp)
                    newName = "有重复！"
                    flag = True
                    break
            # 无法识别姓名
            else:
                flag = False
                newName = ""
        # 解析失败，次数+1
        if flag == False:
            j = j + 1
        if flag == True:
            i = i + 1
        if reFlag == True:
            print("filename=" + filename + "-->" + newName + "，成功=" + str(i) + "，失败=" + str(j))
            print("耗时=" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
def read_directory_pool(filename):
    i = 0
    j = 0
    flag = True  # 用于判断成功、失败+1
    newName = ""
    regex_str = "(^.*?[姓].*?[名].*?)"
    directory_name=r"C:\Users\musaxi\Desktop\照片"
    reFlag = True  # 用于判断有重复数据，就不在答应成功、失败数据
    img = Image.open(directory_name + "/" + filename)
    text = pytesseract.image_to_string(img, lang='chi_sim')
    match_obj = re.match(regex_str, text.replace("\n",""))
    if (match_obj == None):
        img = img.convert('L')  # 转成灰度
        text = pytesseract.image_to_string(img, lang='chi_sim')
        match_obj = re.match(regex_str, text.replace("\n",""))
    if (match_obj == None):
        img_db = Image.open(directory_name + "/" + filename)
        enh_con = ImageEnhance.Contrast(img_db)  # 增强对比度
        contrast = 5.5
        img_db = enh_con.enhance(contrast)
        text = pytesseract.image_to_string(img_db, lang='chi_sim')
        match_obj = re.match(regex_str, text.replace("\n",""))
    if (match_obj == None):
        img_dbhd = Image.open(directory_name + "/" + filename)  # 灰度+对比度
        img_dbhd = img_dbhd.convert("L")
        enh_con = ImageEnhance.Contrast(img_dbhd)  # 增强对比度
        contrast = 5.5
        img_dbhd = enh_con.enhance(contrast)
        text = pytesseract.image_to_string(img_dbhd, lang='chi_sim')
    textarr = text.split("\n")
    k = 0  # 用于取数组值
    for strTp in textarr:
        k = k + 1
        strTemp = strTp.replace(" ", "")
        filenameTp = filename[filename.find("."):len(filename)]
        if strTemp.find("姓名") >= 0:
            if strTemp[3:len(strTemp)] == "":  # 判断姓名:姓名
                newName = "无法识别" + str(uuid.uuid1())
                flag = False
            # 判断姓名不在同一行，识别在第18个数字。
            if strTemp[3:len(strTemp)] == "" and textarr[k].replace(" ", "").find("身份") >= 0:
                try:
                    if len(textarr[18].replace(" ", "")) > 4:
                        tpName = textarr[k + 3].replace(" ", "")
                    else:
                        tpName = textarr[18].replace(" ", "")
                    os.rename(directory_name + "/" + filename,
                              directory_name + "/" + tpName + filenameTp)
                    flag = True
                    newName = tpName
                    break
                except FileExistsError as e:
                    uuidName = "_" + str(uuid.uuid1())
                    os.rename(directory_name + "/" + filename,
                              directory_name + "/" + newName + uuidName + filenameTp)
                    newName = "有重复！"
                    flag = True
                    break
                break  # 识别成功就不在判断后续值
            else:
                newName = strTemp[3:len(strTemp)]
            try:
                newName = newName.replace(":", "")
                os.rename(directory_name + "/" + filename,
                          directory_name + "/" + newName + filenameTp)
                flag = True
                break
            except FileExistsError as e:
                # 有重复的改成重复—+uuid
                uuidName = "_" + str(uuid.uuid1())
                os.rename(directory_name + "/" + filename,
                          directory_name + "/" + newName + uuidName + filenameTp)
                newName = "有重复！"
                flag = True
                break
        # 无法识别姓名
        else:
            flag = False
            newName = ""
    # 解析失败，次数+1
    if flag == False:
        j = j + 1
    if flag == True:
        i = i + 1
    if reFlag == True:
        print("filename=" + filename + "-->" + newName + "，成功=" + str(i) + "，失败=" + str(j))
def read_directory_thread(images):
    directory_name=r"C:\Users\musaxi\Desktop\健康码8.31\8_30学生及家长健康码照片"
    i = 0
    j = 0
    flag = True  # 用于判断成功、失败+1
    newName = ""
    regex_str = "(^.*?[姓].*?[名].*?)"
    for filename in images:
        reFlag = True  # 用于判断有重复数据，就不在答应成功、失败数据
        img = Image.open(directory_name + "/" + filename)
        text = pytesseract.image_to_string(img, lang='chi_sim')
        match_obj = re.match(regex_str, text.replace("\n",""))
        if (match_obj == None):
            img = img.convert('L')  # 转成灰度
            text = pytesseract.image_to_string(img, lang='chi_sim')
            match_obj = re.match(regex_str, text.replace("\n",""))
        if (match_obj == None):
            img_db = Image.open(directory_name + "/" + filename)
            enh_con = ImageEnhance.Contrast(img_db)  # 增强对比度
            contrast = 5.5
            img_db = enh_con.enhance(contrast)
            text = pytesseract.image_to_string(img_db, lang='chi_sim')
            match_obj = re.match(regex_str, text.replace("\n",""))
        if (match_obj == None):
            img_dbhd = Image.open(directory_name + "/" + filename)  # 灰度+对比度
            img_dbhd = img_dbhd.convert("L")
            enh_con = ImageEnhance.Contrast(img_dbhd)  # 增强对比度
            contrast = 5.5
            img_dbhd = enh_con.enhance(contrast)
            text = pytesseract.image_to_string(img_dbhd, lang='chi_sim')
        textarr = text.split("\n")
        k = 0  # 用于取数组值
        for strTp in textarr:
            k = k + 1
            strTemp = strTp.replace(" ", "")
            filenameTp = filename[filename.find("."):len(filename)]
            if strTemp.find("姓名") >= 0:
                if strTemp[3:len(strTemp)] == "":  # 判断姓名:姓名
                    newName = "无法识别" + str(uuid.uuid1())
                    flag = False
                # 判断姓名不在同一行，识别在第18个数字。
                if strTemp[3:len(strTemp)] == "" and textarr[k].replace(" ", "").find("身份") >= 0:
                    try:
                        if len(textarr[18].replace(" ", "")) > 4:
                            tpName = textarr[k + 3].replace(" ", "")
                        else:
                            tpName = textarr[18].replace(" ", "")
                        os.rename(directory_name + "/" + filename,
                                  directory_name + "/" + tpName + filenameTp)
                        flag = True
                        newName = tpName
                        break
                    except FileExistsError as e:
                        uuidName = "_" + str(uuid.uuid1())
                        os.rename(directory_name + "/" + filename,
                                  directory_name + "/" + newName + uuidName + filenameTp)
                        newName = "有重复！"
                        flag = True
                        break
                    break  # 识别成功就不在判断后续值
                else:
                    newName = strTemp[3:len(strTemp)]
                try:
                    newName = newName.replace(":", "")
                    os.rename(directory_name + "/" + filename,
                              directory_name + "/" + newName + filenameTp)
                    flag = True
                    break
                except FileExistsError as e:
                    # 有重复的改成重复—+uuid
                    uuidName = "_" + str(uuid.uuid1())
                    os.rename(directory_name + "/" + filename,
                              directory_name + "/" + newName + uuidName + filenameTp)
                    newName = "有重复！"
                    flag = True
                    break
            # 无法识别姓名
            else:
                flag = False
                newName = ""
        # 解析失败，次数+1
        if flag == False:
            j = j + 1
        if flag == True:
            i = i + 1
        if reFlag == True:
            print("filename=" + filename + "-->" + newName + "，成功=" + str(i) + "，失败=" + str(j))
            print("耗时=" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
#read_directory(path)
