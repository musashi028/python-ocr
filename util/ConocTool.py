import datetime
from cnstd import CnStd
from cnocr import CnOcr
import os
std = CnStd()
cn_ocr = CnOcr()
path=r"C:\Users\musaxi\Desktop\test"
import time
def read_directory(directory_name):
    for filename in os.listdir(directory_name):
        box_info_list = std.detect(directory_name + "/" + filename)
        for box_info in box_info_list:
            cropped_img = box_info['cropped_img']  # 检测出的文本框
            ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
            print('ocr result: %s' % ''.join(ocr_res))
read_directory(path)
