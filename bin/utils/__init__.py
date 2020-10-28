from datetime import date, datetime

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


async def week_number():
    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day
    
    number_of_week = date(year=year, month=month, day=day).isocalendar()[1]
    
    return number_of_week


async def get_timetable(class_id):
    CREDENTIALS_FILE = 'data/api_token.json'
    
    with open('data/sheet_id') as file:
        spreadsheet_id = file.read()

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
    
    week = await week_number()
    
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
        return values['values']
    except:
        return None
