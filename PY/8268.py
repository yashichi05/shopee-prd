import requests
import json
import time
from bs4 import BeautifulSoup
from googlesheet import delsheet
from googlesheet import getsheet
from googlesheet import writesheet
import xlrd

url = 'https://8268.com.tw/product_preorder.php'
post_data = {'account': 'daiyi1200@gmail.com','passwd': 'mj015974','verification': '','exec': 'member_account_login'}

WebSession = requests.Session()
WebSession.post('https://8268.com.tw/all_ajax_login.php',data = post_data) #傳送登入資料
WebSession.get('https://8268.com.tw/') #確定登入


result = WebSession.get(url) #第一次訪問
soup = BeautifulSoup(result.text, "html.parser") 

gotdata = []
for i in soup.select(".product-sort")[1].select('li'):  #分類迴圈
    link = 'https://8268.com.tw'+i.select('a')[0]['href'][1:] #商品分類網址
    if link == 'https://8268.com.tw/product_preorder.php' or link == 'https://8268.com.tw/product_uptodate.php':
        print('忽略預購、新上架')
        continue
    sort_result = WebSession.get(link)  #訪問分頁網址
    sort_soup = BeautifulSoup(sort_result.text, "html.parser") #第二次訪問
    try:
        page_num = int(sort_soup.select('.pager li a')[-1]['href'].split("=")[-1]) #取得分類頁數
    except:#如果錯誤，代表只有一頁
        page_num = 1 
    for page in range(1,page_num+1): #頁數迴圈
        if page_num == 1: #如果分類只有一頁 page 前'?','&'會錯誤
            page_result = WebSession.get(link+'?page_num='+str(page)) #瀏覽內頁
        else:
            page_result = WebSession.get(link+'&page_num='+str(page)) #瀏覽內頁
        page_soup = BeautifulSoup(page_result.text, "html.parser")#第三次訪問

        for ii in page_soup.select('.product_name'): #搜尋產品名迴圈
            try: #有些沒ID 則'無權限'
                gotdata.append([ii['href'].split("=")[1].split("&")[0],ii.text,ii.find_next_siblings('div')[1].text.replace("$",""),ii.find_next_sibling('div').text.replace("庫存：","")])

            except:
                gotdata.append(['無權限',ii.text,ii.find_next_siblings('div')[1].text.replace("$",""),ii.find_next_sibling('div').text.replace("庫存：","")])
                
            print(ii.text)

id_data = []
for i in gotdata: #提取ID 資料
    id_data.append(i[0])

#讀取excel 資料
#產生google 寫入資料
xlrd.Book.encoding = "utf8" #设置编码
data = xlrd.open_workbook(r"C:\Users\Owner\Desktop\shopee prd\productsID.xlsx")
table1 = data.sheet_by_index(0) #取第一张工作簿
rows_count = table1.nrows #取总行数
wriso = [] #更新標題
for i in range(rows_count):
    wriso.append([table1.cell_value(i,0),table1.cell_value(i,1),table1.cell_value(i,2)])

wrval = [] #寫入的資料
for row in range(rows_count):
    wrval.append([""])
    
for row in range(rows_count):
    try:
        stock_count = gotdata[id_data.index(table1.cell_value(row,18))][3] #取得庫存數量
        stock_count = int(stock_count)*int(table1.cell_value(row,19)) #庫存數乘以箱入數
        wrval[row] = [stock_count]
    except:
        pass

wrval[0][0] = "官網" + time.strftime("%m/%d", time.localtime())
delsheet("庫存表!E:E")
writesheet("庫存表!A1",wriso)
writesheet("庫存表!E1",wrval)
print("OK")