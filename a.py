from datetime import date, datetime, timedelta


today = datetime.today()
date_now = date(year=today.year, month=today.month, day=today.day)

week = date_now.isocalendar()[1]
weekday = datetime.isoweekday(today)

time = int(datetime.time(today).strftime('%H'))

if weekday >= 5 and time >= 8:
    week += 1

day = date(today.year, 1, 1)

if day.weekday() <= 3 :
    day -= timedelta(day.weekday())             
else:
    day += timedelta(7 - day.weekday())
    
dt = timedelta(days=((week - 1) * 7))

monday = (day + dt).strftime('%d.%m.%Y')
sunday = (day + dt + timedelta(days=6)).strftime('%d.%m.%Y')



print(monday, sunday)