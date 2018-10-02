from bs4 import BeautifulSoup
import tkinter as tk
import requests
import json

def pconeID(pdid):

    url = "https://www.pcone.com.tw/product/info/"+pdid
    my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    gotrq = requests.get(url,headers = my_headers)
    soup = BeautifulSoup(gotrq.text, "html.parser") #"html.parser" html解析器 將html 轉為bs4格式操作
    strnum = soup.select('script')[23].text.find("window._pc_p = ") #提取JSON資料
    gotjson = soup.select('script')[23].text[strnum+len("window._pc_p = "):-2]
    load = json.loads(gotjson)  #轉成python dict

    for i in range(len(load['volumes'])):
        output.insert(1.0,str(load['volumes'][i]['volume_id'])+"   "+str(load['volumes'][i]['volume_remaining'])+" "+str(load['volumes'][i]['option'])+"\n")


def clickbtn():
    try:
        output.delete('1.0',tk.END)
    except:
        print("start")
    inputID = IDinput.get()
    pconeID(inputID)

    
gui=tk.Tk()
gui.title("查松果ID")
output= tk.Text()
output.pack()
IDinput = tk.Entry()
IDinput.pack()
btn = tk.Button(gui, text ="執行", command = clickbtn)
btn.pack(anchor='center', expand='yes')
gui.mainloop()