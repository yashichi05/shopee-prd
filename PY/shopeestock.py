#蝦皮庫存
import xlrd
import time
import tkinter as tk
import tkinter.filedialog as filedialog
import os
from googlesheet import delsheet
from googlesheet import getsheet
from googlesheet import writesheet


def browser():
    fname = filedialog.askopenfilename(initialdir= os.getcwd(),filetypes = (("Excel","*.xlsx"),("all files","*.*")))
    global filepath
    filepath =  fname  # 返回文件全路径
    pathinput.delete('0',tk.END)
    pathinput.insert(0,filepath)
    
    #print(filedialog.askdirectory())  # 返回目录路径
    
def shopeeExcel(path):
    xlrd.Book.encoding = "utf8" #设置编码
    data = xlrd.open_workbook(path)
    table = data.sheet_by_index(0) #取第一张工作簿
    rows_count = table.nrows #取总行数
    prdid = []
    for row in range(rows_count):#無款式
        if table.cell(row,0).value:
            try:
                prdid.append({"ID":str(int(table.cell(row,0).value)),"stock":str(int(table.cell(row,6).value))})
            except:
                a = "a"
    for i in range(20):
        col = 5*i
        for row in range(rows_count): #商品款式
            try:
                prdid.append({"ID":str(int(table.cell(row,8+col).value)),"stock":str(int(table.cell(row,12+col).value))})
            except:
                a = "b"
    return prdid
def run():
    print(filepath)
    delsheet("商品ID!R:R")
    getidlist = getsheet("商品ID!I:J")
    oklist = shopeeExcel(filepath) #讀取EXCEL
    #提取sheet 資料
    sprdid = []
    smodelid = []
    for i in range(len(getidlist)):
        try:
            sprdid.append(getidlist[i][0])
        except:
            sprdid.append("")
        try:
            smodelid.append(getidlist[i][1])
        except:
            smodelid.append("")
        
    #尋找並寫入sheet
    wrval = []
    noidlist = []

    for i in range(len(getidlist)):
        wrval.append([""])
    for i in range(len(oklist)):

        try:
            findrow = sprdid.index(oklist[i]["ID"])
            wrval[findrow] = [oklist[i]["stock"]]
        except:
            try:
                findrow = smodelid.index(oklist[i]["ID"])
                wrval[findrow] = [oklist[i]["stock"]]
            except:
                noidlist.append(oklist[i]["ID"])

    wrval[0] = ["Shopee"+ time.strftime("%m/%d", time.localtime())]
    writesheet("商品ID!R1",wrval)

gui=tk.Tk()
gui.title("更新蝦皮庫存")
gui.geometry("450x50")
pathinput = tk.Entry(width=50)
pathinput.pack(side="left")
btn2 = tk.Button(gui, text ="瀏覽", command = browser)
btn2.pack(side="left")
btn = tk.Button(gui, text ="執行", command = run)
btn.pack(side="left")
gui.mainloop()

