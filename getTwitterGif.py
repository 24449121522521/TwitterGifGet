import requests
from bs4 import BeautifulSoup
import re
import os

# 获取网页源码
def getHTMLText(url):
    """
    url : 需要爬取的 Twitter 链接
    return : 返回网页源码或空字符串
    """
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()
        r.encoding = "utf-8"
        return r.text
    except:
        return ""

# 获取图片对应的 mp4 链接
def getMP4Link(html):
    """
    html : 网页源码
    return : 返回 mp4 链接中的关键信息
    """
    soup = BeautifulSoup(html,"html.parser")
    for tag in soup.find_all("meta",property = "og:image"):
        img = tag.get("content")
    # 正则表达式匹配出关键信息，并修改扩展名
    key = re.findall(r'\w+.jpg',img)
    key = key[0].replace("jpg","mp4")
    return key

# 下载 mp4 视频
def download(link,path):
    """
    link : 需要下载的 mp4 视频的链接
    path : 下载的视频存储路径
    """
    try:
        print("准备下载视频.........")
        response = requests.get(link)
        data = response.content
        if data:
            if not os.path.exists(path):
                print("文件保存在：{}".format(path))
                with open(path,'wb') as f:
                    f.write(data)
                    f.close()
                    print("视频下载成功!!!")
            else:
                print("文件已存在")
    except Exception as e:
        print(e)
        print("下载失败")
    finally:
        print("程序结束")
                    
    
def main():
    url = input("请输入带有 Gif 图片的 Twitter 链接 : ")
    path = input("请输入保存路径 : ")
   
    prefix = "https://video.twimg.com/tweet_video/"
    html = getHTMLText(url)
    key = getMP4Link(html)
    link = prefix + key
    
    download(link,path)

if __name__ == "__main__":
    main()
    
