from datetime import date, datetime, timedelta


async def week_number(next_week):
    today = datetime.today()
    date_now = date(year=today.year, month=today.month, day=today.day)

    week = date_now.isocalendar()[1]
    weekday = datetime.isoweekday(today)

    time = int(datetime.time(today).strftime('%H'))

    if weekday >= 5 and time >= 8:
        week += 1

    if next_week is True:
        week += 1

    return week


async def start_end_week(next_week):
    day = date(datetime.today().year, 1, 1)
    week = await week_number(next_week)

    if day.weekday() <= 3:
        day -= timedelta(day.weekday())
    else:
        day += timedelta(7 - day.weekday())

    dt = timedelta(days=((week - 1) * 7))

    date_monday = (day + dt).strftime('%d.%m.%Y')
    date_sunday = (day + dt + timedelta(days=6)).strftime('%d.%m.%Y')

    return date_monday, date_sunday
