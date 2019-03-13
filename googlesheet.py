from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
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