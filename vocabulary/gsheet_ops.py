from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '16XwTneCe03ek7Efp3V7YYvkvxRLDsEOvbTzXOMYRBMA'
SAMPLE_RANGE_NAME = 'Sheet1!A1:D'

def get_authenticated_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'env/gsheets/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def gsheet_append(gsheet_service, gsheet_id, gsheet_range, insert_data_option, value_input_option, body):
    sheet = gsheet_service.spreadsheets()
    sheet.values().append(spreadsheetId=gsheet_id,
                            range=gsheet_range,
                            insertDataOption=insert_data_option,
                            valueInputOption=value_input_option,
                            body=body).execute()

def gsheet_get(gsheet_service, gsheet_id, gsheet_range):
    sheet = gsheet_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=gsheet_id,
                                range=gsheet_range).execute()
    return result.get('values',[])

if __name__ == '__main__':
    service = get_authenticated_service()
    gsheet_append(service, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME, 'INSERT_ROWS', 'RAW', {'values':[
                                    ['test','test_pos','test_mean','test_syn']
                                ]})
    res = gsheet_get(service, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
    print(res)