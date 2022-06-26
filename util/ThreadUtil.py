import datetime
import multiprocessing  # 引用进程模块
import os
import threading  # 引用线程模块
import time
import concurrent.futures
from multiprocessing.pool import Pool

from util.Pytesseract import read_directory_thread
# mult = multiprocessing.Process(target=func, args=(1314,))
# mult.start()  # 运行进程
if __name__ == '__main__':
    start = time.time()
    print("start="+str(start))
    print("耗时=" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    #cpu多线程自动控制执行
    #p = concurrent.futures.ProcessPoolExecutor()
    #p.map(read_directory_thread,os.listdir(r"C:\Users\musaxi\Desktop\照片"))
    #多线程执行
    # pool = Pool(8)
    # pool.map(read_directory_thread, os.listdir(r"C:\Users\musaxi\Desktop\照片"))
    # pool.close()
    # pool.join()

# thre1 = threading.Thread(target=read_directory, args=(r"C:\Users\musaxi\Desktop\照片\1",))  # 创建一个线程
# thre1.start()  # 运行线程
# thre2 = threading.Thread(target=read_directory, args=(r"C:\Users\musaxi\Desktop\照片\2",))   # 创建一个线程
# thre2.start()  # 运行线程
##thre3 = threading.Thread(target=read_directory, args=(r"C:\Users\musaxi\Desktop\照片\3",))  # 创建一个线程
# thre3.start()  # 运行线程
# thre4 = threading.Thread(target=read_directory, args=(r"C:\Users\musaxi\Desktop\照片\4",))   # 创建一个线程
# thre4.start()  # 运行线程
    imgs = os.listdir(r"C:\Users\musaxi\Desktop\照片")
    thre=[]
    j=30
    num= int(len(imgs)/j)
    if(len(imgs)%j!=0):
        num=num+1
    #最快都要60s，从3分钟提升到60s。
    for i in range(j):
        if(i*num<len(imgs)):
            print(i * num, (i + 1) * num - 1)
            if(i==j):
                threading.Thread(target=read_directory_thread, args=(imgs[len(imgs)-i*num:len(imgs)],)).start()
            else:
                threading.Thread(target=read_directory_thread, args=(imgs[i * num:(i + 1) * num - 1],)).start()  # 创建一个线程
        i = i + 1
    end = time.time()
    print("end=" + str(end))
    print(end - start)