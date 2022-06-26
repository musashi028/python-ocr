import base64
import datetime
import os
import uuid

import requests


class CodeDemo:
    def __init__(self, AK, SK, code_url, img_path):
        self.AK = AK
        self.SK = SK
        self.code_url = code_url
        self.img_path = img_path
        self.access_token = self.get_access_token()

    def get_access_token(self):
        token_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={ak}&client_secret={sk}'.format(
            ak=self.AK, sk=self.SK)
        header = {'Content-Type': 'application/json; charset=UTF-8'}
        response = requests.post(url=token_host, headers=header)
        content = response.json()
        access_token = content.get("access_token")
        return access_token

    def getCode(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        def read_img():
            with open(self.img_path, "rb")as f:
                return base64.b64encode(f.read()).decode()

        image = read_img()
        response = requests.post(url=self.code_url, data={"image": image, "access_token": self.access_token},
                                 headers=header)
        return response.json()


if __name__ == '__main__':
    i = 0
    j = 0
    path = r"C:\Users\musaxi\Desktop\照片"
    AK = "AK"  # 官网获取的AK
    SK = "SK"  # 官网获取的SK
    code_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"  # 高进度识别
    #code_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate"  # 高进度含位置
    # code_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"  # 标准识别
    # code_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"  # 标准含位置
    for filename in os.listdir(path):
        reFlag = True  # 用于判断有重复数据，就不在答应成功、失败数据
        img_path = path + "/" + filename  # 识别图片的地址
        code_obj = CodeDemo(AK=AK, SK=SK, code_url=code_url, img_path=img_path)
        res = code_obj.getCode()
        resStr = ""
        for reStrTp in res.get("words_result"):
            resStr = resStr + str(reStrTp.get("words"))+"\n"
        textarr = resStr.split("\n")
        k = 0  # 用于取数组值
        for strTp in textarr:
            k = k + 1
            strTemp = strTp.replace(" ", "")
            filenameTp = filename[filename.find("."):len(filename)]
            if strTemp.find("姓名") >= 0:
                if strTemp[3:len(strTemp)] == "":  # 判断姓名:姓名
                    newName = "无法识别" + str(uuid.uuid1())
                    flag = False
                if strTemp[3:len(strTemp)] == "":
                    try:
                        tpName = textarr[k].replace(" ", "")
                        os.rename(path + "/" + filename,
                                  path + "/" + tpName + filenameTp)
                        flag = True
                        newName = tpName
                        break
                    except FileExistsError as e:
                        uuidName = "_" + str(uuid.uuid1())
                        os.rename(path + "/" + filename,
                                  path + "/" + newName + uuidName + filenameTp)
                        newName = "有重复！"
                        flag = True
                        break
                    break  # 识别成功就不在判断后续值
                else:
                    newName = strTemp[3:len(strTemp)]
                try:
                    newName = newName.replace(":", "")
                    os.rename(path + "/" + filename,
                              path + "/" + newName + filenameTp)
                    flag = True
                    break
                except FileExistsError as e:
                    # 有重复的改成重复—+uuid
                    uuidName = "_" + str(uuid.uuid1())
                    os.rename(path + "/" + filename,
                              path + "/" + newName + uuidName + filenameTp)
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