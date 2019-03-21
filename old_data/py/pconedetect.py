import requests
import json
import time
import tkinter as tk
from bs4 import BeautifulSoup
from googlesheet import delsheet
from googlesheet import getsheet
from googlesheet import writesheet

def clickbtn():
    try:
        output.delete('1.0',tk.END)
    except:
        print("start")
    pconedetect()

    
def pconedetect():

    url = "https://www.pcone.com.tw/api/merchant/products?items_per_page=1000&merchant_id=2945567&page=1"
    my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    gotrq = requests.get(url,headers = my_headers)
    data = json.loads(gotrq.text)  #轉成python dict
    pconeIDAry = []
    for i in range(len(data["products"])):
        pconeIDAry.append(data["products"][i]["display_id"])
    
    GOTData = getsheet('商品ID!O:O') #獲取試算表所有資料
    GOTDataAry = []
    errorID = []
    for i in range(len(GOTData)):
        try:
            GOTDataAry.append(GOTData[i][0])  #提取試算表資料
        except:
            GOTDataAry.append("") #空直例外
    for i in range(len(pconeIDAry)):#找網頁上架ID在不在 試算表中
        try:
            GOTDataAry.index(pconeIDAry[i])
        except: #找不到的話
            errorID.append(pconeIDAry[i])
    for i in range(len(errorID)):
        output.insert(1.0,str(errorID[i])+"\n")
    output.insert(1.0,"偵測完成\n")




gui=tk.Tk()
gui.title("查松果新上架")
output= tk.Text()
output.pack()
btn = tk.Button(gui, text ="執行", command = clickbtn)
btn.pack(anchor='center', expand='yes')
gui.mainloop()