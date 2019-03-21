#露天全部
import requests
import json
import time
from bs4 import BeautifulSoup
from googlesheet import delsheet
from googlesheet import getsheet
from googlesheet import writesheet


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

def getruten(pid):
    url = "https://goods.ruten.com.tw/item/show?"+pid
    my_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    gotrq = requests.get(url,headers = my_headers)
    soup = BeautifulSoup(gotrq.text, "html.parser") #"html.parser" html解析器 將html 轉為bs4格式操作
    strnum = soup.select('script[type="text/javascript"]')[15].text.find("RT.context = ") #提取JSON資料 #find 找到RT.context的位址
    gotjson = soup.select('script[type="text/javascript"]')[15].text[strnum+len("RT.context = "):-2]
    load = json.loads(gotjson)  #轉成python dict
    outObj = {"state":"0","prd":""}
    prdAry = []
    if load['item']['specInfo']: #是否有款式
        for k,v in load['item']['specInfo']['specs'].items():#for 出dict 資料
            prdAry.append([k,v['spec_num'],v['spec_name'],v["spec_status"]])
            #print(k+':'+v['spec_num']+" "+v['spec_name']+v["spec_status"])
        outObj["prd"]=prdAry
    else:
        outObj["prd"]=str(load['item']['remainNum'])
        #print(load['remain_count'])
    outObj["state"] = load['item']['isSoldEnd']
    return outObj

def getALLRuten():
    prdidData = getsheet('商品ID!G:H') #獲取試算表所有資料
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
                gotstock = getruten(prdidData[row][0]) #讀取網頁
                if type(gotstock['prd']) == type(""): #如果prd為文字則為無款式
                     wrval[row] = [gotstock['prd']]
                else:#有款式
                    for i in range(len(gotstock["prd"])):
                        if gotstock["prd"][i][0] == prdidData[row][1]: #有找到款式ID
                            wrval[row] = [gotstock["prd"][i][1]] #寫入資料
                            if gotstock["prd"][i][3] == "N": #如果發現款式是關閉
                                wrval[row]=["款式關閉"]
                    if wrval[row] == "":#都沒有找到
                        wrval[row] = ["款式ID錯誤"]
                if gotstock["state"] == True:
                    wrval[row] = ["下架"]
        except: #有可能ID錯誤，有可能ID無值
            try:
                if prdidData[row][0]:#ID錯誤
                    wrval[row] = ["商品ID錯誤或無款式ID"]
            except:
                wrval[row] = [""]
    wrval[0][0] = "Ruten" + time.strftime("%m/%d", time.localtime())#寫入第一列
    delsheet("商品ID!T:T") #刪除原有資料
    writesheet("商品ID!T1",wrval) #寫入資料
    return wrval
    print("OK")

getALLRuten()