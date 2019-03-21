#蝦皮總上架ID
import tkinter as tk
import requests
import json
from googlesheet import delsheet
from googlesheet import getsheet
from googlesheet import writesheet

def updateSPID():
    webidAry = []
    my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    for i in range(200):
        url = "https://shopee.tw/api/v2/search_items/?by=pop&limit=100&match_id=2019696&newest="+str(i*100) +"&order=desc&page_type=shop"
        gotrq = requests.get(url,headers = my_headers)
        loadjson = json.loads(gotrq.text)
        if len(loadjson["items"]) == 0:
            break
        for ct in range(len(loadjson["items"])):
            webidAry.append(loadjson["items"][ct]["itemid"])

    #比對新增的WEBID
    GOTData = getsheet('商品ID!I:I') #獲取試算表所有資料
    IDAry = [] #已上的ID
    errorAry = [] #找到的未上ID
    for i in range(len(GOTData)): #提取資料
        try:
            IDAry.append(GOTData[i][0])
        except:
            IDAry.append("")
    for i in range(len(webidAry)): #找到未上的ID
        try:
            IDAry.index(str(webidAry[i]))
        except:
            errorAry.append(webidAry[i])
    
    output.insert(1.0,"查詢完成\n")
    for i in range(len(errorAry)):
        output.insert(1.0,str(errorAry[i])+"\n")


        

def clickbtn():
    try:
        output.delete('1.0',tk.END)
    except:
        print("start")
    updateSPID()
    
    
gui=tk.Tk()
gui.title("查蝦皮新上架")
output= tk.Text()
output.pack()
btn = tk.Button(gui, text ="執行", command = clickbtn)
btn.pack(anchor='center', expand='yes')
gui.mainloop()