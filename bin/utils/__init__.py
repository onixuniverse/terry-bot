from datetime import date, datetime, timedelta

import apiclient.discovery
import httplib2
from loguru import logger
from oauth2client.service_account import ServiceAccountCredentials

from .. import db
from ..src import bot


async def get_channel(guild_id: int):
    channel_id = await db.record('SELECT log_ch FROM channels WHERE guild_id = %s', guild_id)
    if channel_id:
        channel = bot.get_channel(channel_id)
        
        return channel


async def get_role(guild_id: int, role: str):
    guild = bot.get_guild(guild_id)
    
    role_id = await db.record(f'SELECT {role} FROM roles WHERE guild_id = %s', guild_id)
    if role_id:
        role = guild.get_role(role_id)
        
        return role


async def get_guest_role(guild_id: int):
    guest_role = await get_role(guild_id, 'guest_role')
    
    return guest_role


async def get_curator_role(guild_id: int):
    curator_role = await get_role(guild_id, 'curator_role')
    
    return curator_role


async def week_number(next_week):
    
    today = datetime.today()
    date_now = date(year=today.year, month=today.month, day=today.day)

    week = date_now.isocalendar()[1]
    weekday = datetime.isoweekday(today)

    time = int(datetime.time(today).strftime('%H'))

    if weekday >= 5 and time >= 8:
        week += 1
    if next_week:
        week += 1    
        
    today = datetime.today()
    first_day = date(today.year, 1, 1)

    if first_day.weekday() <= 3 :
        first_day -= timedelta(first_day.weekday())             
    else:
        first_day += timedelta(7 - first_day.weekday())
        
    dt = timedelta(days=((week - 1) * 7))

    monday = first_day + dt
    sunday = first_day + dt + timedelta(days=6)

    return week, monday, sunday


async def get_timetable(class_id, next_week):
    CREDENTIALS_FILE = 'data/api_token.json'
    
    with open('data/sheet_id') as file:
        spreadsheet_id = file.read()

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
    
    week, monday, sunday = await week_number(next_week)
    
    if week % 2 == 1:
        class_id = class_id + '_1'
    elif week % 2 == 0:
        class_id = class_id + '_2'
    else:
        logger.error('Something went wrong.')
    
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{class_id}!B2:G10',
        majorDimension='COLUMNS'
    ).execute()
    
    try:
        return values['values'], monday, sunday
    except:
        return None, monday, sunday

async def generate_timetable(class_id, next_week):
        values, monday, sunday = await get_timetable(class_id, next_week)
        timetable = {}
        
        if values:
            try:
                timetable = {
                    'time': values[0],
                    'monday': values[1],
                    'thuesday': values[2],
                    'wednesday': values[3],
                    'thursday': values[4],
                    'friday': values[5],
                }
                
                for table in timetable:
                    new_table = '\n'.join(timetable[table])
                    
                    timetable[table] = new_table
            except Exception as exc:
                logger.error(exc)
                    
        return timetable, monday, sunday
