from typing import Optional

from bin.utils.dates import start_end_week
from bin.utils.timetables import generate_timetable
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands.core import command
from resources.data.config import PREFIX


async def gen_timetable_embed(timetable):

    emb = Embed()
    emb.set_thumbnail(
        url='https://img.icons8.com/dusk/64/000000/timetable.png')

    fields = [('Время занятий', timetable['time'], True),
              ('Понедельник', timetable['monday'], True),
              ('Вторник', timetable['thuesday'], True),
              ('Среда', timetable['wednesday'], True),
              ('Четверг', timetable['thursday'], True),
              ('Пятница', timetable['friday'], True)]

    for name, value, inline in fields:
        emb.add_field(name=name, value=value, inline=inline)

    return emb


class Timetable(Cog):
    """Timetable cog"""
    def __init__(self, bot):
        self.bot = bot

    @command(name='table',
             aliases=['расписание', 'расп', 'Расписание', 'Расп'],
             brief='Расписание уроков')
    async def send_timetable(self, ctx, class_id: Optional[str]):
        """Отправляет расписание уроков на текущую неделю
        `[class_id]`: класс"""

        if class_id and (ctx.guild.id == 693730890261463050 or ctx.guild.id == 696734117873713172):
            timetable = await generate_timetable(class_id, False)

            if timetable:
                date_monday, date_sunday = await start_end_week(False)

                emb = await gen_timetable_embed(timetable)
                emb.color = 0x1BFF00
                emb.title = 'Расписание уроков'
                emb.description = f'Расписание дейстивтельно с {date_monday} по {date_sunday}'
                emb.set_footer(text=f'Чтобы увидеть расписание на следующую неделю введите: {PREFIX}распслед {class_id}')

                await ctx.send(embed=emb)

            else:
                await ctx.send(f'Расписание для класса {class_id} не найдено.'
                               f'\nЧтобы его получить введите: `{PREFIX}расписание [класс]`')

        else:
            await ctx.send(f'**[E]** | Не удалось найти указанный класс __{class_id}__.')

    @command(name='tablenext', aliases=['рслед', 'Рслед', 'распслед', 'Распслед'],
             brief='Расписание уроков на следующую неделю')
    async def send_timetable_next(self, ctx, class_id: Optional[str]):
        """Отправляет расписание уроков на следующую неделю
        `[class_id]`: класс"""

        if class_id and (ctx.guild.id == 693730890261463050 or ctx.guild.id == 696734117873713172):
            timetable = await generate_timetable(class_id, True)

            if timetable:
                date_monday, date_sunday = await start_end_week(True)

                emb = await gen_timetable_embed(timetable)
                emb.color = 0xFF8F00
                emb.title = 'Расписание уроков __на следующую неделю__'
                emb.description = f'Расписание дейстивтельно с {date_monday} по {date_sunday}'
                emb.set_footer(text=f'Чтобы увидеть расписание на следующую неделю введите: {PREFIX}расписание {class_id}')

                await ctx.send(embed=emb)

            else:
                await ctx.send(f'Расписание для класса {class_id} на следующую неделю не найдено.'
                               f'\nЧтобы его получить введите: `{PREFIX}расписание [класс]`')

        else:
            await ctx.send(f'**[E]** | Не удалось найти указанный класс __{class_id}__.')


def setup(bot):
    bot.add_cog(Timetable(bot))
