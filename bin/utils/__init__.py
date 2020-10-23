import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

from ..src import bot
from .. import db


async def get_channel(guild_id: int):
    channel_id = await db.record('SELECT log_ch FROM channels WHERE guild_id = %s', guild_id)
    if channel_id:
        channel = bot.get_channel(channel_id)
        
        return channel


async def get_role(guild_id: int):
    guild = bot.get_guild(guild_id)
    
    role_id = await db.record('SELECT guest_role FROM roles WHERE guild_id = %s', guild_id)
    if role_id:
        role = guild.get_role(role_id)
        
        return role

async def get_timetable(class_id: str=None):
    if class_id:
        CREDENTIALS_FILE = 'data/api_token.json'
        
        with open('data/sheet_id') as file:
            spreadsheet_id = file.read()

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f'{class_id}!B2:F10',
            majorDimension='COLUMNS'
        ).execute()

        try:
            return values['values']
        except:
            return None
