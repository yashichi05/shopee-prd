#查庫存ID GUI 露天
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

def rutenID(rid):

    url = "https://goods.ruten.com.tw/item/show?"+rid
    my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    gotrq = requests.get(url,headers = my_headers)
    soup = BeautifulSoup(gotrq.text, "html.parser") #"html.parser" html解析器 將html 轉為bs4格式操作
    strnum = soup.select('script[type="text/javascript"]')[15].text.find("RT.context = ") #提取JSON資料 #find 找到RT.context的位址
    gotjson = soup.select('script[type="text/javascript"]')[15].text[strnum+len("RT.context = "):-2]
    load = json.loads(gotjson)  #轉成python dict
    if load['item']['specInfo']: #是否有款式
        for k,v in load['item']['specInfo']['specs'].items():#for 出dict 資料
            try:
                output.insert(1.0,'\n'+str(v['spec_ext']['goods_no']))
            except:
                print("款式沒有國際條碼")
            output.insert(1.0,'\n'+k+' :'+v['spec_num']+" "+v['spec_name'])
            output.insert(1.0,'\n')
    else:
         output.insert(1.0,'\n'+str(load['item']['remainNum']))
    output.insert(1.0,'\n'+remove_emoji(load['item']['name']))
    output.insert(1.0,"下架了嗎?"+str(load['item']['isSoldEnd']))
    

def clickbtn():
    try:
        output.delete('1.0',tk.END)
    except:
        print("start")
    inputID = IDinput.get()
    rutenID(inputID)

    
gui=tk.Tk()
gui.title("查露天ID")
output= tk.Text()
output.pack()
IDinput = tk.Entry()
IDinput.pack()
btn = tk.Button(gui, text ="執行", command = clickbtn)
btn.pack(anchor='center', expand='yes')
gui.mainloop()