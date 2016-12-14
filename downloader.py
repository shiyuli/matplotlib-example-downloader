# encoding: utf-8
# using Python 3.5
from bs4 import BeautifulSoup as BS
from urllib import request
import os

# 下载函数
def download(target):
    baseUrl = "http://matplotlib.org/examples/"
    url = target['href']

    # 文件夹名称
    dirName = url[:url.find(r'/')]

    # 判断文件夹是否存在，不存在则创建
    if not os.path.exists('examples'+'\\'+dirName):
        os.system('mkdir examples'+'\\'+dirName)

    response = request.urlopen(baseUrl+url).read()
    soup = BS(response, 'html.parser', from_encoding='utf-8')

    # 获取新打开页面的下载对象的URL，不存在则返回
    try:
        fileName = soup.find('a', class_='external')['href']
        print('Trying {}'.format(fileName))
    except:
        return

    # 完整的URL，可以直接用来下载
    wholeFileUrl = baseUrl + dirName + '/' + fileName

    # 文件内容
    file = request.urlopen(wholeFileUrl).read()

    makeFile(file, fileName, dirName)
    print('File {} done!'.format(fileName))

# 文件生成函数
def makeFile(file, fileName, dirName):
    fileName = checkFileName(fileName)
    try:
        f = open('examples/'+dirName+'/'+fileName, 'wb')
    except:
        return
    f.write(file)
    f.close()

# 文件名校验函数
def checkFileName(fileName):
    # 如果找不到'/'的话返回原名
    if fileName.find('/') == -1:
        return fileName

    # 通过最后一个'/'的索引获取文件名
    index = []
    i = 0
    for fileNameChar in fileName:
        if fileNameChar == '/':
            index.append(i)
        i += 1
    index = index[len(index)-1]
    return fileName[index+1:]

# 断点续传功能
def makeBreakPoint(breakPoint, mode):
    with open('breakPoint.ini', mode) as f:
        if mode == 'r':
            breakPoint = f.read().strip()
            f.close()
            return breakPoint
        elif mode == 'w':
            f.write(breakPoint)
            f.close()

if __name__ == "__main__":
    html = open('source.html', 'r')
    soup = BS(html, 'html.parser', from_encoding='utf-8')
    targets = soup.find('div', id='target').find_all('a')

    # 可以自行设置断点，如果为空则从配置中读取
    breakPoint = ""
    if breakPoint == "":
        breakPoint = makeBreakPoint(breakPoint, 'r')
    if breakPoint:
        breakPointDone = False
        for target in targets:
            if target.string == breakPoint:
                download(target)
                breakPointDone = True
            elif breakPointDone:
                breakPoint = target.string
                makeBreakPoint(breakPoint, 'w')
                download(target)
