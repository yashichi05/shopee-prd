import requests
import json
import time
from bs4 import BeautifulSoup
from googlesheet import delsheet
from googlesheet import getsheet
from googlesheet import writesheet


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

def getyahoo(pid):
    url = "https://tw.bid.yahoo.com/item/"+pid
    my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    gotrq = requests.get(url,headers = my_headers)
    soup = BeautifulSoup(gotrq.text, "html.parser") #"html.parser" html解析器 將html 轉為bs4格式操作
    #for item in soup.select(".listing-title"): #html 可以使用select 選擇想要的東西
    #print(item.select("a")[0].text)
    gotjson = soup.select("#isoredux-data")[0].get("data-state") #get 取得屬性
    load = json.loads(gotjson)  #轉成python dict
    outObj = {"state":"0","prd":""}
    if len(load["item"]["specs"]) == 0:
        #print(load["item"]["models"][0]["id"]+":"+ str(load["item"]["models"][0]["qty"]))
        outObj["prd"] = str(load["item"]["models"][0]["qty"])
    else:
        outAry = []
        for i in range(len(load["item"]["models"])): #提取ID
            specnameID = str(load["item"]["models"][i]["specCombination"]).split(":")
            specname = str(load["item"]["specs"][0]['options'][i]['name'])
            outAry.append([str(load["item"]["models"][i]["id"]),str(load["item"]["models"][i]["qty"]),specname])
            #print(load["item"]["models"][i]["id"]+":"+ str(load["item"]["models"][i]["qty"])+" "+specname)
            outObj["prd"] = outAry
            
    outObj["state"] = str(load["item"]["status"])    
    return outObj

def getALLYahoo():
    prdidData = getsheet('商品ID!E:F') #獲取試算表所有資料
    wiAry=[]
    tiAry= []
    wrval = [] #寫入的陣列

    for row in range(len(prdidData)):#新增同列數陣列
        wrval.append([""])
    
    for row in range(len(prdidData)):
    #for row in range(5,12):
        print(str(row)+"/"+str(len(prdidData))) #進度
        try:
            if prdidData[row][0]:
                gotstock = getyahoo(prdidData[row][0])
                if type(gotstock['prd']) == type(""): #如果prd為文字則為無款式
                     wrval[row] = [gotstock['prd']]
                else:#有款式
                    for i in range(len(gotstock["prd"])):
                        if gotstock["prd"][i][0] == prdidData[row][1]:
                            wrval[row] = [gotstock["prd"][i][1]]
                    if wrval[row] == "":#都沒有找到
                        wrval[row] = ["款式ID錯誤"]
                if gotstock["state"] == '3':
                    wrval[row] = ["下架"]
        except: #有可能ID錯誤，有可能ID無值
            try:
                if prdidData[row][0]:#ID錯誤
                    wrval[row] = ["商品ID錯誤或無款式ID"]
            except:
                wrval[row] = [""]
    wrval[0][0] = "Yahoo" + time.strftime("%m/%d", time.localtime())
    delsheet("商品ID!S:S")
    writesheet("商品ID!S1",wrval)
    return wrval
    print("OK")
	
	

	
getALLYahoo()