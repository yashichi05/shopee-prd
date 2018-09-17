#第一次執行需要用CMD執行 才會跑出網頁認證
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

def main():
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
    RANGE_NAME = '停售!A1'
    values =[['AAA']]
    body = {'values': values}
    print(body)

    value_input_option = 'USER_ENTERED'
    result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME,valueInputOption=value_input_option,body=body).execute()
    print(result)


if __name__ == '__main__':
    main()