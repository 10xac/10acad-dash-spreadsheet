import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials as sac
import pandas as pd


def gsheet2df(spreadsheet_name, sheet_num):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials_path = 'appli.json'

    credentials = sac.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(credentials)

    sheet = client.open(spreadsheet_name).get_worksheet(sheet_num).get_all_records()
    df = pd.DataFrame.from_dict(sheet)

    return df

def main():
    df = gsheet2df('10 Academy Batch 4 Application form (Responses)', 0)
    df['Timestamp'] = df['Timestamp'].apply(lambda x: datetime.datetime.strptime(x, "%d/%m/%Y %H:%M:%S"))

    df['date'] = df['Timestamp'].dt.date
    df['date'] = df['date'].apply(lambda x: str(x))

    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(days=1))

    dfYes = df[df['date'] == yesterday]
    return yesterday, dfYes.shape[0]

if __name__ == '__main__':
    main()
