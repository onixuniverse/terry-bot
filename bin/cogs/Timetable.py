from data.config import PREFIX
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands.core import command

from ..utils import generate_timetable


class Timetable(Cog):
    """Timetable cog"""
    def __init__(self, bot):
        self.bot = bot
    
    @command(name='timetable',
           aliases=['timetables', 't', 'расписание', 'р', 'расп', 'рсп', 'Расписание', 'Р', 'Расп'])
    async def send_timetable(self, ctx, class_id: str=None):
        """Send timetable for this week."""
        if class_id:
            timetable, monday, sunday = await generate_timetable(class_id, False)
            
            if timetable:
                emb = Embed(color=0xAAFF43, title='Расписание уроков')
                emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/timetable.png')
                emb.description = f'Расписание дейстивтельно с {monday} по {sunday}'
                emb.set_footer(text=f'Чтобы увидеть расписание на следующую неделю введите: {PREFIX}рслед {class_id}')
                
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
        else:
            await ctx.send(f'**[E]** | Не удалось найти указанный класс __{class_id}__. ' + \
                            'Существующие классы: **5А, 5Б, 5В, 5Г, 6А, 6Б, 6В, 7А, 7Б, 7В, ' + \
                            '8А, 8Б, 8В, 9А, 9Б, 10, 11.**')
        
    @command(name='timetable_next',
             aliases=['timetablenext', 'tn', 'расписаниеследующее',
                      'рс', 'рслед', 'Рслед', 'РСлед', 'распслед',
                      'Расписаниеследующее', 'РС', 'Распслед', 'РаспСлед',
                      'распс'])
    async def send_timetable_next(self, ctx, class_id: str=None):
        """Send timetable for next week."""
        if class_id:
            timetable, monday, sunday = await generate_timetable(class_id, True)
            
            if timetable:
                emb = Embed(color=0xFFAF43, title='Расписание уроков __на следующую неделю__')
                emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/timetable.png')
                emb.description = f'Расписание дейстивтельно с {monday} по {sunday}.'
                emb.set_footer(text=f'Чтобы увидеть расписание на эту неделю: {PREFIX}расписание {class_id}')
                
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
                await ctx.send(f'Расписание для класса {class_id} на следующую неделю не найдено.\nЧтобы его получить введите: `{PREFIX}расписание [класс]`')
        else:
            await ctx.send(f'**[E]** | Не удалось найти указанный класс __{class_id}__. ' + \
                            'Существующие классы: **5А, 5Б, 5В, 5Г, 6А, 6Б, 6В, 7А, 7Б, 7В, ' + \
                            '8А, 8Б, 8В, 9А, 9Б, 10, 11.**')


def setup(bot):
    bot.add_cog(Timetable(bot))
