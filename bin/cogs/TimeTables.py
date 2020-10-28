from typing import Optional
from discord import Embed
from discord.ext.commands import Cog, command

from ..utils import get_timetable


class TimeTable(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name='timetable',
             aliases=['timetables', 'расписание', 'рс', 'расп'])
    async def send_timetable(self, ctx, class_id: Optional[str]):
        if class_id:
            values = await get_timetable(class_id)
            
            if values:
                timetables = {
                    'time': values[0],
                    'monday': values[1],
                    'thuesday': values[2],
                    'wednesday': values[3],
                    'thursday': values[4],
                    'friday': values[5],
                }
                
                # for table in timetables:
                #     for i in range(len(timetables[table])):
                #         if timetables[table][i] == '':
                #             timetables[table][i] = '\_\_\_\_\_'
                
                for table in timetables:
                    new_table = '\n'.join(timetables[table])
                    
                    timetables[table] = new_table
                
                emb = Embed(color=0xAAFF43,
                            title='Расписание')
                emb.add_field(name='Время занятий', value=timetables['time'], inline=True)
                emb.add_field(name='Понедельник', value=timetables['monday'], inline=True)
                emb.add_field(name='Вторник', value=timetables['thuesday'], inline=True)
                emb.add_field(name='Среда', value=timetables['wednesday'], inline=True)
                emb.add_field(name='Четверг', value=timetables['thursday'], inline=True)
                emb.add_field(name='Пятница', value=timetables['friday'], inline=True)
                emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/timetable.png')
                # emb.set_footer(text='_____ - окно')
                await ctx.send(embed=emb)
            
            else:
                await ctx.send('**[E]** | Указанного расписания не найдено.')


def setup(bot):
    bot.add_cog(TimeTable(bot))
