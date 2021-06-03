import pprint
import getAppli
import datetime
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'ganal.json'
VIEW_ID = '188831196'

def init_analyticsReporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)

    # Build the service object
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics

def getSessReport(analytics):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '2021-05-31', 'endDate': '2021-06-01'}],
                    'metrics': [{'expression': 'ga:sessions'}],
                    'dimensions': [{'name': 'ga:country'}]
                }
            ]
        }
    ).execute()

def getUserReport(analytics):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '1daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:users'}],
                    'dimensions': [{'name': 'ga:userType'}]
                }
            ]
        }
    ).execute()

def getSessDurReport(analytics):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '2021-05-31', 'endDate': '2021-06-01'}],
                    'metrics': [{'expression': 'ga:avgSessionDuration'}],
                    'dimensions': [{'name': 'ga:sessionDurationBucket'}]
                }
            ]
        }
    ).execute()

def printResponse(key, response):
    # print(f'\n\n {key} \n\n')
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        # for row in report.get('data', {}).get('rows', []):
        #     dimensions = row.get('dimensions', [])
        #     dateRangeValues = row.get('metrics', [])

        #     for header, dimension in zip(dimensionHeaders, dimensions):
        #         print(header + ': ', dimension)

        #     for i, values in enumerate(dateRangeValues):
        #         print(values)
        #         print('Date range:', str(i))
        #         for metricHeader, value in zip(metricHeaders, values.get('values')):
        #             print(metricHeader.get('name') + ' : ', value)

        for total in report.get('data', {}).get('totals', []):
            for metricHeader, value in zip(metricHeaders, total.get('values')):
                # print(f"total number of {metricHeader.get('name')} : {value}")
                total = value

    return total

def convertToMinutes(seconds):
    seconds = float(seconds)
    seconds = round(seconds)
    return str(datetime.timedelta(seconds=seconds))

def main():
    analytics = init_analyticsReporting()
    Sessresponse = getSessReport(analytics)
    sessDurResponse = getSessDurReport(analytics)
    userResponse = getUserReport(analytics)

    responses = {
        'Number of Sessions': Sessresponse,
        'Average Session Duration': sessDurResponse,
        'Number of Users': userResponse
    }

    totalSess = printResponse('Number of Sessions', Sessresponse)
    avgSessDur = printResponse('Average Session Duration', sessDurResponse)
    avgSessDur = convertToMinutes(avgSessDur)
    totalUser = printResponse('Number of Users', userResponse)
    date, totalAppli = getAppli.main()

    print(f'{date}\t{totalSess}\t{avgSessDur}\t{totalUser}\t{totalAppli}')

    return (date, totalUser, totalSess, avgSessDur, totalAppli)

if __name__ == '__main__':
    main()
