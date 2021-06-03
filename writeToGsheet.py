import os.path
import getGanal
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '17j09p3RCJMUEquWNt_B6lXSWxQ4SXxJVU4mH-ntnEN8'
RANGE_NAME = 'Weekly Inputs!A2:E'


def init_sheets():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gsheet.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    return service

def main():
    service = init_sheets()
    sheet = service.spreadsheets()
    value_input_option = "USER_ENTERED"
    insert_data_option = "INSERT_ROWS"
    values = [
        list(getGanal.main())
    ]

    body = {
        'values': values
    }

    result = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                                   valueInputOption=value_input_option, insertDataOption=insert_data_option,
                                   body=body).execute()

if __name__ == '__main__':
    main()
