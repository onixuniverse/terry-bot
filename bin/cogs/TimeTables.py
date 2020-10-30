from data.config import PREFIX
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands.core import command

from ..utils import generate_timetable


class TimeTable(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name='timetable',
           aliases=['timetables', 'tt', 'расписание', 'р', 'расп',
                    'Расписание', 'Р', 'Расп'],
           enabled=True)
    async def send_timetable(self, ctx, class_id: str=None, next_week: str=None):
        if class_id:
            title = 'Расписание уроков'
            
            if next_week:
                next_week = True
                title = 'Расписание уроков __на следующую неделю__'
                
            timetable, monday, sunday = await generate_timetable(class_id, next_week)
            
            if timetable:
                emb = Embed(color=0xAAFF43, title=title)
                emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/timetable.png')
                emb.description = f'Расписание дейстивтельно с {monday} по {sunday}'
                emb.set_footer(text=f'Чтобы увидеть расписание на следующую неделю введите: {PREFIX}расписание {class_id} <любой символ>')
                
                fields = [('Время занятий', timetable['time'], True),
                        ('Понедельник', timetable['monday'], True),
                        ('Вторник', timetable['thuesday'], True),
                        ('Среда', timetable['wednesday'], True),
                        ('Четверг', timetable['thursday'], True),
                        ('Пятница', timetable['friday'], True)]
                
                for name, value, inline in fields:
                    emb.add_field(name=name, value=value, inline=inline)
                
                await ctx.send(embed=emb)
                
            else:
                await ctx.send(f'Расписание для класса {class_id} не найдено.\nЧтобы его получить введите: `{PREFIX}расписание [класс]`')
            
def setup(bot):
    bot.add_cog(TimeTable(bot))
