from typing import Optional

from loguru import logger

from data.config import PREFIX
from discord import Embed
from discord.ext.commands import Cog, command

from ..utils import get_timetable


class TimeTable(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name='timetable',
             aliases=['timetables', 'расписание', 'рс', 'расп'])
    async def send_timetable(self, ctx, class_id: Optional[str], next_week: Optional[bool]=False):
        if class_id:
            values = await get_timetable(class_id, next_week)
            
            if values:
                try:
                    timetables = {
                        'time': values[0],
                        'monday': values[1],
                        'thuesday': values[2],
                        'wednesday': values[3],
                        'thursday': values[4],
                        'friday': values[5],
                    }
                    
                    for table in timetables:
                        new_table = '\n'.join(timetables[table])
                        
                        timetables[table] = new_table
                    
                    emb = Embed(color=0xAAFF43, title='Расписание')
                    emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/timetable.png')
                    emb.set_footer(text=f'Чтобы увидеть расписание на следующую неделю введите: {PREFIX}расписание {class_id} True')
                    
                    fields = [('Время занятий', timetables['time'], True),
                            ('Понедельник', timetables['monday'], True),
                            ('Вторник', timetables['thuesday'], True),
                            ('Среда', timetables['wednesday'], True),
                            ('Четверг', timetables['thursday'], True),
                            ('Пятница', timetables['friday'], True)]
                    
                    for name, value, inline in fields:
                        emb.add_field(name=name, value=value, inline=inline)
                    
                    await ctx.send(embed=emb)
                    
                except IndexError as exc:
                    logger.error(exc)
                    await ctx.send(f'Расписание для класса {class_id} не найдено.\nЧтобы его получить введите: `{PREFIX}расписание [класс]`')
        else:
            await ctx.send(f'Расписание для класса {class_id} не найдено.\nЧтобы его получить введите: `{PREFIX}расписание [класс]`')

def setup(bot):
    bot.add_cog(TimeTable(bot))
