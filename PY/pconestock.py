from __future__ import print_function
from bs4 import BeautifulSoup
from selenium import webdriver
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import requests
import json
import time

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


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
        except:
            try:
                if prdidData[row][0]:
                    wrval[row] = ["錯誤或下架"]
            except:
                wrval[row] = [""]
    wrval[0][0] = "Pcone" + time.strftime("%m/%d", time.localtime())
    writesheet("商品ID!Q1",wrval)
    print("OK")
	
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
	
def delsheet(sheetrange):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    SPREADSHEET_ID = '19ZXwhENPrLmLURoKO4xXoCDahpyMG5wuU_8xsU74kyI'
    RANGE_NAME = {'ranges' : [sheetrange]}
    result = service.spreadsheets().values().batchClear(spreadsheetId=SPREADSHEET_ID,body=RANGE_NAME).execute()
    print(result)
def getsheet(sheetrange):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    SPREADSHEET_ID = '19ZXwhENPrLmLURoKO4xXoCDahpyMG5wuU_8xsU74kyI'
    RANGE_NAME = sheetrange
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        return values

def writesheet(sheetrange,writeVal):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    SPREADSHEET_ID = '19ZXwhENPrLmLURoKO4xXoCDahpyMG5wuU_8xsU74kyI'
    RANGE_NAME = sheetrange
    values =[['=52+25']]
    body = {'values': writeVal}
    value_input_option = 'USER_ENTERED'
    result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME,valueInputOption=value_input_option,body=body).execute()
    print(result)
	
getALLpcone()