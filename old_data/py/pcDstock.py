#PCD ALL
import requests
import json
import time
from bs4 import BeautifulSoup
from googlesheet import delsheet
from googlesheet import getsheet
from googlesheet import writesheet


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

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
            prdAry.append([v['p_sseq'],v['p_invt'],v['p_spec']])
    else:#舊的都是陣列
        for i in range(len(load)):
            prdAry.append([load[i]['p_sseq'],load[i]['p_invt'],load[i]['p_spec']])
    outObj["prd"] = prdAry
    return outObj

def getALLpcd():
    prdidData = getsheet('商品ID!M:N') #獲取試算表所有資料
    wiAry=[]
    tiAry= []
    wrval = []

    for row in range(len(prdidData)):
        wrval.append("")
    
    for row in range(len(prdidData)):
        print(str(row)+"/"+str(len(prdidData)))
        try:
            if prdidData[row][0]:
                time.sleep(0.5) #PC會檔大量讀取
                gotstock = getpcd(prdidData[row][0]) #gotstock 得到PC網頁的資料
                for i in range(len(gotstock["prd"])): #依網頁資料款式的種類數量迴圈
                    if gotstock["prd"][i][0] == prdidData[row][1]:#獲取的款式ID 等於 試算表上的款式ID
                        wrval[row] = [gotstock["prd"][i][1]] #指派數量資料
                if wrval[row] == "":
                    wrval[row] = ["款式ID錯誤"]
            else:
                wrval[row] = ["商品ID錯誤"]
        except:
            try:
                if prdidData[row][0]:
                    wrval[row] = ["錯誤或下架"]
            except:
                wrval[row] = [""]
    wrval[0][0] = "PC大一" + time.strftime("%m/%d", time.localtime())
    delsheet("商品ID!U:U")
    writesheet("商品ID!U1",wrval)
    print("OK")

getALLpcd()