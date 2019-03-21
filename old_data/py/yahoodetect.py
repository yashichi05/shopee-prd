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
    added_thread = threading.Thread(target=yahoodetect) #添加多線呈
    # 執行 thread
    added_thread.start()


    
def yahoodetect():
    allid = []
    for page in range(1,200):
        try:
            output.insert(1.0,".")
            url = "https://tw.bid.yahoo.com/booth/Green-Forest-Y3489416698?bfe=1&page="+str(page)
            my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
            gotrq = requests.get(url,headers = my_headers)
            soup = BeautifulSoup(gotrq.text, "html.parser") #"html.parser" html解析器 將html 轉為bs4格式操作
            yahoohtml = soup.find_all('div','item-wrap')
            if len(yahoohtml) == 0 : #找完跳出
                break
            for i in range(len(yahoohtml)):
                allid.append(yahoohtml[i]['data-mid'])    

        except:
            print("end")
            break
    output.insert(1.0,"\n")
    GOTData = getsheet('商品ID!E:E')
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
gui.title("雅虎新上架")
output= tk.Text()
output.pack()
btn = tk.Button(gui, text ="執行", command = clickbtn)
btn.pack(anchor='center', expand='yes')
gui.mainloop()



   