import re
import urllib.request

# ------ 获取网页源代码的方法 ---
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html

# ------ getHtml()内输入任意帖子的URL ------
html = getHtml("http://test.com")
# ------ 修改html对象内的字符编码为UTF-8 ------
html = html.decode('UTF-8')

# ------ 获取帖子内所有图片地址的方法 ------
def getImg(html):
    # ------ 利用正则表达式匹配网页内容找到图片地址 ------
    reg = r'src="([.*\S]*\.jpg)"'
    imgre = re.compile(reg);
    imglist = re.findall(imgre, html)
    return imglist

imgList = getImg(html)
imgName = 0
for imgPath in imgList:
    # ------ 这里最好使用异常处理及多线程编程方式 ------
    try:
        f = open('c:\\Users\\musaxi\\Desktop\\1'+ str(imgName)+".jpg", 'wb')
        f.write((urllib.request.urlopen(imgPath)).read())
        print(imgPath)
        f.close()
    except Exception as e:
        print(imgPath+" error")
    imgName += 1

print("All Done!")