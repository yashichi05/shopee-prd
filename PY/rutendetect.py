#查雅虎新增
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
    added_thread = threading.Thread(target=rutendetect) #添加多線呈
    # 執行 thread
    added_thread.start()


    
def rutendetect():
    allid = []
    for page in range(1,200):
        output.insert(1.0,".")
        url = "http://class.ruten.com.tw/user/index00.php?s=ting865290&p="+str(page)
        my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        gotrq = requests.get(url,headers = my_headers)
        soup = BeautifulSoup(gotrq.text, "html.parser") #"html.parser" html解析器 將html 轉為bs4格式操作
        rutenhtml = soup.find_all('div','rt-product-tag-container tagging-class')
        end = soup.find_all("div",class_ = "item-img-wrap")
        for i in range(len(rutenhtml)):
            allid.append(rutenhtml[i]['name'])
        if len(end) == 0:
            break

    output.insert(1.0,"\n")
    GOTData = getsheet('商品ID!G:G')
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
gui.title("露天新上架")
output= tk.Text()
output.pack()
btn = tk.Button(gui, text ="執行", command = clickbtn)
btn.pack(anchor='center', expand='yes')
gui.mainloop()



   