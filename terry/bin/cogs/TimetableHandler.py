from typing import Optional

from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands.core import command

from terry.resources.data.config import PREFIX
from ..utils import generate_timetable, start_end_week


async def gen_timetable_embed(timetable):
    emb = Embed()
    emb.set_thumbnail(url='https://img.icons8.com/dusk/64/000000/timetable.png')

    fields = [('Время занятий', timetable['time'], True),
              ('Понедельник', timetable['monday'], True),
              ('Вторник', timetable['thursday'], True),
              ('Среда', timetable['wednesday'], True),
              ('Четверг', timetable['thursday'], True),
              ('Пятница', timetable['friday'], True)]

    for name, value, inline in fields:
        emb.add_field(name=name, value=value, inline=inline)

    return emb


class TimetableHandler(Cog):
    """Timetable cog"""
    def __init__(self, bot):
        self.bot = bot

    @command(name='table', aliases=['расписание', 'расп', 'Расписание', 'Расп', 'р', 'Р'], brief='Расписание уроков')
    async def send_timetable(self, ctx, class_id: Optional[str]):
        """Отправляет расписание уроков на текущую неделю
        `[class_id]`: класс"""
        if ctx.guild.id == 693730890261463050 or ctx.guild.id == 696734117873713172:
            if class_id:
                timetable = await generate_timetable(class_id, False)

                if timetable:
                    date_monday, date_sunday = await start_end_week(False)

                    emb = await gen_timetable_embed(timetable)
                    emb.color = 0x1BFF00
                    emb.title = 'Расписание уроков'
                    emb.description = f'Расписание действительно с {date_monday} по {date_sunday}'
                    emb.set_footer(text=f'Чтобы увидеть расписание на следующую неделю введите: '
                                        f'{PREFIX}распслед {class_id}')

                    await ctx.send(embed=emb)
                else:
                    await ctx.send(f'Расписание для класса {class_id} не найдено.\nЧтобы его получить введите: '
                                   f'`{PREFIX}расписание [класс]`')
            else:
                await ctx.send(('**[E]** | Не удалось найти указанный класс', class_id))
        else:
            await ctx.send('К сожалению, функция расписания временно не доступна на сторонних северах.\nМы оповестим '
                           'вас, когда она станет вновь доступна.')

    @command(name='tablenext', aliases=['распслед', 'рс', 'Рс'], brief='Расписание уроков на следующую неделю')
    async def send_timetable_next(self, ctx, class_id: Optional[str]):
        """Отправляет расписание уроков на следующую неделю
        `[class_id]`: класс"""
        if ctx.guild.id == 693730890261463050 or ctx.guild.id == 696734117873713172:
            if class_id:
                timetable = await generate_timetable(class_id, True)

                if timetable:
                    date_monday, date_sunday = await start_end_week(True)

                    emb = await gen_timetable_embed(timetable)
                    emb.color = 0xFF8F00
                    emb.title = 'Расписание уроков __на следующую неделю__'
                    emb.description = f'Расписание действительно с {date_monday} по {date_sunday}'
                    emb.set_footer(text=f'Чтобы увидеть расписание на текущую неделю введите: {PREFIX}расп{class_id}')

                    await ctx.send(embed=emb)
                else:
                    await ctx.send(f'Расписание для класса {class_id} на следующую неделю не найдено.'
                                   f'\nЧтобы его получить введите: `{PREFIX}расписание [класс]`')
            else:
                await ctx.send(('**[E]** | Не удалось найти указанный класс', class_id))
        else:
            await ctx.send('К сожалению, функция расписания временно не доступна на сторонних северах.\nМы оповестим '
                           'вас, когда она станет вновь доступна.')


def setup(bot):
    bot.add_cog(TimetableHandler(bot))
