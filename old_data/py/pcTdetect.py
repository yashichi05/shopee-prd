#PC 新上架
from bs4 import BeautifulSoup
import tkinter as tk
import requests
import json
import threading #多線呈
from googlesheet import delsheet
from googlesheet import getsheet
from googlesheet import writesheet

def clickbtn():
    try:
        output.delete('1.0',tk.END)
    except:
        print("start")
    added_thread = threading.Thread(target=pcddetect) #添加多線呈
    # 執行 thread
    added_thread.start()


    
def pcddetect():
    allid = []
    for page in range(1,200):
        #登錄後才能訪問的網頁
        url = 'http://seller.pcstore.com.tw/S163498400/plist_dt.htm?s=S163498400&c=&skw=&pg='+str(page)+'&sr=1&pp=50' 

        #瀏覽器登錄後得到的cookie，也就是剛才複製的字符串
        cookie_str = r'cbj=IqhLsP6..LOKMq6kVcXtnWgBVcXtnqojj' #######################這邊要研究
        my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}


        #把cookie字符串處理成字典，以便接下來使用
        cookies = {}
        for line in cookie_str.split(';'): #cookie_str.split(';') 依分號 分割成陣列 並列出

            key, value = line.split('=', 1) #將陣列依序指派給key value
            cookies[key] = value #新增物件
        session = requests.Session()
        res = session.get(url,cookies=cookies,headers = my_headers)
        soup = BeautifulSoup(res.text, "html.parser") #"html.parser" html解析器 將html 轉為bs4格式操作
        html = soup.find_all('a','hotProdList')
        for link in html:
            linkID = link['href'].replace('/S163498400/','').replace('.htm','')
            allid.append(linkID)

        if len(html) < 50:
            break     
    output.insert(1.0,"\n")
    GOTData = getsheet('商品ID!K:K')
    takeid = []
    for i in range(len(GOTData)):
        try:
            takeid.append(GOTData[i][0])
        except:
            continue
    errorid = []
    for i in range(len(allid)):
        try:
            takeid.index(allid[i]) #看試算表尚存不存在網頁ID
        except:
            output.insert(1.0,str(allid[i])+"\n")
    output.insert(1.0,"偵測完成\n")



gui=tk.Tk()
gui.title("PC梓原新上架")
output= tk.Text()
output.pack()
btn = tk.Button(gui, text ="執行", command = clickbtn)
btn.pack(anchor='center', expand='yes')
gui.mainloop()



   