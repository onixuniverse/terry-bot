import os

import googleapiclient.discovery
import httplib2
from loguru import logger
from oauth2client.service_account import ServiceAccountCredentials

from .dates import week_number


async def get_timetable(class_id, next_week):
    credentials_file = 'terry/resources/data/tokens/googleapi_token.json'
    spreadsheet_id = os.getenv("SHEET_ID")

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    http_auth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http=http_auth)

    week = await week_number(next_week)

    if week % 2 == 1:
        class_id = class_id + '_1'  # если неделя нечетная
    elif week % 2 == 0:
        class_id = class_id + '_2'  # если неделя четная

    try:
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f'{class_id}!B2:G10',
            majorDimension='COLUMNS'
        ).execute()['values']
    except Exception as exc:
        values = None
        logger.error(exc)

    return values


async def generate_timetable(class_id, next_week):
    values = await get_timetable(class_id, next_week)
    timetable = {}

    if values:
        try:
            timetable = {
                'time': values[0],
                'monday': values[1],
                'tuesday': values[2],
                'wednesday': values[3],
                'thursday': values[4],
                'friday': values[5],
            }

            for table in timetable:
                new_table = '\n'.join(timetable[table])

                timetable[table] = new_table
        except Exception as exc:
            logger.error(exc)

    return timetable
