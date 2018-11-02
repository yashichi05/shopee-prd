#查庫存ID GUI 雅虎
from bs4 import BeautifulSoup
import tkinter as tk
import requests
import json
import re
def remove_emoji(data):#去除emojis
    if not data:
        return data
    try:
    # UCS-4
        patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
    # UCS-2
        patt = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
    return patt.sub('', data)
def yahooID(yid):

    url = "https://tw.bid.yahoo.com/item/"+yid
    my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    gotrq = requests.get(url,headers = my_headers)
    soup = BeautifulSoup(gotrq.text, "html.parser") #"html.parser" html解析器 將html 轉為bs4格式操作
    #for item in soup.select(".listing-title"): #html 可以使用select 選擇想要的東西
        #print(item.select("a")[0].text)
    gotjson = soup.select("#isoredux-data")[0].get("data-state") #get 取得屬性
    load = json.loads(gotjson)  #轉成python dict
    if len(load["item"]["specs"]) != 0:
        for i in range(len(load["item"]["models"])): #提取ID
            specnameID = str(load["item"]["models"][i]["specCombination"]).split(":")
            specname = str(load["item"]["specs"][0]['options'][i]['name'])
            if specnameID[1] == str(load["item"]["specs"][0]['options'][i]['id']):
                text = ' 驗證成功'
            else:
                text = ' 驗證失敗'

            output.insert(1.0,"\n"+load["item"]["models"][i]["id"]+" :"+ str(load["item"]["models"][i]["qty"])+" "+specname+text)
    else:
        output.insert(1.0,"\n"+str(load["item"]["models"][0]["qty"]))
    output.insert(1.0,"\n"+remove_emoji(load["item"]["title"]))
    output.insert(1.0,str(load["item"]["status"])+"   ● 2:上架,3:下架")
    

def clickbtn():
    try:
        output.delete('1.0',tk.END)
    except:
        print("start")
    inputID = IDinput.get()
    yahooID(inputID)

    
gui=tk.Tk()
gui.title("查雅虎ID")
output= tk.Text()
output.pack()
IDinput = tk.Entry()
IDinput.pack()
btn = tk.Button(gui, text ="執行", command = clickbtn)
btn.pack(anchor='center', expand='yes')
gui.mainloop()