#查庫存ID GUI PCD
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



def getpcd(pid):
    url = "http://seller.pcstore.com.tw/S188431702/"+pid+".htm"
    my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    gotrq = requests.get(url,headers = my_headers)
    soup = BeautifulSoup(gotrq.text, "html.parser") #"html.parser" html解析器 將html 轉為bs4格式操作
    gotjson = soup.select('#specs')[0].text
    load = json.loads(gotjson)
    outObj = {"state":"0","prd":""}
    prdAry = []
    if type(load) == dict: #新上的都是字典檔
        for k,v in load.items():
            output.insert(1.0,"\n"+v['p_spec']+"   "+v['p_sseq']+"  數量:"+v['p_invt'])
    else:#舊的都是陣列
        for i in range(len(load)):
            output.insert(1.0,"\n"+load[i]['p_spec']+"   "+load[i]['p_sseq']+"  數量:"+load[i]['p_invt'])
    outObj["prd"] = prdAry
    output.insert(1.0,"\n")
    output.insert(1.0,remove_emoji(soup.select('.info .tit')[0].get_text()))

def clickbtn():
    try:
        output.delete('1.0',tk.END)
    except:
        print("start")
    inputID = IDinput.get()
    getpcd(inputID)

    
gui=tk.Tk()
gui.title("查PC大一ID")
output= tk.Text()
output.pack()
IDinput = tk.Entry()
IDinput.pack()
btn = tk.Button(gui, text ="執行", command = clickbtn)
btn.pack(anchor='center', expand='yes')
gui.mainloop()