#查庫存ID GUI 露天
from bs4 import BeautifulSoup
import tkinter as tk
import requests
import json

def rutenID(rid):

    url = "https://goods.ruten.com.tw/item/show?"+rid
    my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    gotrq = requests.get(url,headers = my_headers)
    soup = BeautifulSoup(gotrq.text, "html.parser") #"html.parser" html解析器 將html 轉為bs4格式操作
    strnum = soup.select('script[type="text/javascript"]')[16].text.find("RT.context = ") #提取JSON資料 #find 找到RT.context的位址
    gotjson = soup.select('script[type="text/javascript"]')[16].text[strnum+len("RT.context = "):-2]
    load = json.loads(gotjson)  #轉成python dict
    if 'spec_info' in load.keys(): #是否有款式
        for k,v in load['spec_info']['specs'].items():#for 出dict 資料
            try:
                output.insert(1.0,'\n'+str(v['spec_ext']['goods_no']))
            except:
                print("款式沒有國際條碼")
            output.insert(1.0,'\n'+k+' :'+v['spec_num']+" "+v['spec_name'])
            output.insert(1.0,'\n')
    else:
         output.insert(1.0,'\n'+str(load['remain_count']))
    output.insert(1.0,'\n'+load['g_name'])
    output.insert(1.0,"有上架嗎?"+str(load['is_product_buyer']))
    

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