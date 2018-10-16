import requests
import json
import time
from bs4 import BeautifulSoup
from googlesheet import delsheet
from googlesheet import getsheet
from googlesheet import writesheet


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

def getpcone(pid):
    url = "https://www.pcone.com.tw/product/info/"+pid
    my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    gotrq = requests.get(url,headers = my_headers)
    soup = BeautifulSoup(gotrq.text, "html.parser") #"html.parser" html解析器 將html 轉為bs4格式操作
    strnum = soup.select('script')[23].text.find("window._pc_p = ") #提取JSON資料
    gotjson = soup.select('script')[23].text[strnum+len("window._pc_p = "):-2]
    load = json.loads(gotjson)  #轉成python dict
    outObj = {"state":"0","prd":""}
    prdAry = []
    for i in range(len(load['volumes'])):
        prdAry.append([str(load['volumes'][i]['volume_id']),str(load['volumes'][i]['volume_remaining']),str(load['volumes'][i]['option'])])
    outObj["prd"] = prdAry
    return outObj

def getALLpcone():
    delsheet("商品ID!Q:Q")
    prdidData = getsheet('商品ID!O:P') #獲取試算表所有資料
    wiAry=[]
    tiAry= []
    wrval = []

    for row in range(len(prdidData)):
        wrval.append("")
    
    for row in range(len(prdidData)):
        print(str(row)+"/"+str(len(prdidData)))
        try:
            	
            if prdidData[row][0]:
                gotstock = getpcone(prdidData[row][0])
                for i in range(len(gotstock["prd"])):
                    if gotstock["prd"][i][0] == prdidData[row][1]:
                        wrval[row] = [gotstock["prd"][i][1]]
                if wrval[row] == "":
                    wrval[row] = ["款式ID錯誤"]
        except:
            try:
                if prdidData[row][0]:
                    wrval[row] = ["錯誤或下架"]
            except:
                wrval[row] = [""]
    wrval[0][0] = "Pcone" + time.strftime("%m/%d", time.localtime())
    writesheet("商品ID!Q1",wrval)
    print("OK")
	
	

	
getALLpcone()