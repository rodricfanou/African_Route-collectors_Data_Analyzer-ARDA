from datetime import date
from datetime import datetime
from time import *

## Multi-year timescales: multi-years splitted into years
def multiyear():
    yearList = []
    i = 2004
    current_year = date.today().year
    while i < current_year:
        i+=1
        if i not in yearList:
            yearList.append(i)
    return yearList


## last year (Now - 12 months) splitted into months
def lastyear():
    year = date.today().year
    month = date.today().month
    months = year * 12 + month  # Months since year 0 minus 1
    i= 0
    tuples = []
    while i < 13:
        i+=1
        tuples.insert(0, ((months - i) // 12, (months - i) % 12 + 1))
    return tuples


## last month (Now - 4weeks) splitted into weeks
def lastmonth():
    year = date.today().year
    month = date.today().month
    months = year * 12 + month  # Months since year 0 minus 1
    day = date.today().day
    i= 0
    tuples = []
    while i < 1:
        i+=1
        tuples.insert(0, ((months - i) // 12, (months - i) % 12 + 1))
    return tuples



## find the number of the week of a day in a month
def find_week_num_in_month(day_of_month):
    #day_of_month = datetime.datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1
    return week_number



## find the number of the first week of a month in a year
def find_week_num_in_year(year, month, day_of_month):
    import datetime
    week_number = datetime.date(year, month, day_of_month).isocalendar()[1]
    return week_number



##find last day in a month
def last_day_of_month(any_day):
    import datetime
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)
    #for month in range(1, 13):
    #...     print last_day_of_month(datetime.date(2012, month, 1))



## find the beginning and the end of the week
def weekbegend(year, week):
    from datetime import datetime, date, timedelta
    d = date(year, 1, 1)
    delta_days = d.isoweekday() - 1
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    # delta for the beginning of the week
    delta = timedelta(days=-delta_days, weeks=delta_weeks)
    weekbeg = d + delta
    # delta2 for the end of the week
    delta2 = timedelta(days=6-delta_days, weeks=delta_weeks)
    weekend = d + delta2
    return weekbeg, weekend

#weekbeg, weekend = weekbegend(2009, 1)
#begweek = weekbeg.strftime("%A %d %B %Y")
#endweek = weekend.strftime("%A %d %B %Y")



