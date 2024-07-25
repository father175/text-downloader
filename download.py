import requests as r
import time
import os
from bs4 import BeautifulSoup
# 请求头
headers = {
    'Accept-Encoding': 'gbk',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
}
def check(omg):
    for i in omg:
        if i=='_':
            return 0
    return 1
# 多线程下载器（本下载器只可用于顶点小说网）
def run(start,id):
    web="https://www.xkjxw.com"+start
    file=open(id+".txt","w")
    while True:
            # 获取标题
            index = r.get(web, headers=headers)
            index.encoding = 'gbk'
            soup=BeautifulSoup(index.text, 'lxml')
            text=soup.html.body.find("div",attrs={"class":"book read"})
            file.write(("### "+text.find("h1",attrs={"class":"pt10"}).get_text()).encode("gbk").decode("gb18030"))
            # 获取文字内容
            output=str(text.find("div",attrs={"class":"readcontent"}))
            output=output.replace("<div class=\"readcontent\"><div class=\"kongwen\"></div><div class=\"readmiddle\"></div>","")
            output=output.replace("<p>天才一秒记住顶点小说网,<span style=\"color:#4876FF\">www.xkjxw.com</span>,如果被浏览器转码或畅读,内容容易缺失,阅读体验极差,请退出转码或畅读模式。</p>","")
            output=output.replace("<br/>","\n    ")
            output=output.replace("<p class=\"text-danger text-center\">本章未完，点击下一页继续阅读</p>","")
            output=output.replace("</div>","")
            cleaned_output = ''.join(c for c in output if c.encode('gbk', 'ignore').decode('gbk'))  
            file.write(cleaned_output.encode("gbk" ).decode("gb18030"))
            # 跳转页数
            web="https://www.xkjxw.com/8/8577/"+text.find_all("a",attrs={"class":"red"})[4]['href']
            # 判定结尾
            if check(web)==1:
                break
            time.sleep(2.5)
    file.close()
# 目录网址，可以更改
root="https://www.xkjxw.com/txt8577.html"
# 下载目录
index=r.get(root, headers=headers)
index.encoding = 'gbk'
soup=BeautifulSoup(index.text, 'lxml')
mad=soup.html.body.find("div",attrs={"id":"list-chapterAll"}).find_all("a")
print("根目录加载完毕")
# 任务分配系统
for i in mad:
    if i["href"]>="/8/8577/3638323.html":# 开始节点
        print("开始下载"+i["href"])
        run(i["href"],i.text)
