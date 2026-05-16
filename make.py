import datetime, time, calendar
from datetime import date

current_year = datetime.datetime.now().year

months = ["", "January", "February", "March",
          "April", "May", "June",
          "July", "August", "September",
          "October", "November", "December"]

blank = '<div class="blank-page"></div>'
style = '<link rel="stylesheet" href="style.css">'

with open("year.html", "r") as year:
    year = year.read()

with open("month.html", "r") as month:
    month = month.read()

with open("week.html", "r") as week:
    week = week.read()


def weekgen(isow, cyear=current_year):
    output = []
    for d in range(1, 8):
        day = date.fromisocalendar(cyear, isow, d)
        output.append(months[day.month])
        output.append(str(day.day))
    return output

output = [style, blank, year]
    
for m in range(1, 13):
    end = ""
    a, b, c = "", "", ""
    dim = calendar.monthrange(current_year, m)[1]
    if dim > 28:
        a = "29"
        if dim > 29:
            b = "30"
            if dim > 30:
                c = "31"
    this_month = month.format(a, b, c, months[m])
    output.append(this_month)
    
    start_week = date(current_year, m, 1).isocalendar().week
    end_week = date(current_year, m, dim).isocalendar().week
    # Catch if all the weeks in the month are actually there
    # Sometimes ISO weeks include Jan 1 / Dec 31 in the "wrong year" 
    if start_week > end_week and m == 1:
        days = weekgen(start_week, int(current_year - 1))
        days.append(start_week)
        output.append(week.format(*days))
        start_week = 1
    elif start_week > end_week and m == 12:
        days = weekgen(end_week, int(current_year + 1))
        days.append(end_week)
        end_week = date(current_year, 12, 28).isocalendar()[1]
        end = week.format(*days)
        
    for w in range(start_week, end_week+1):
        days = weekgen(w)
        # If Thursday is not in the current month... skip it,
        # unless we're at the start or end of the year
        if days[6] != months[m]:
            if days[6] == "December" \
               and months[m] == "January":
                pass
            elif days[6] == "January" \
                 and months[m] == "December":
                pass
            else:
                continue
        days.append(w)
        output.append(week.format(*days))
    output.append(end)

output.append(blank)
output = "\n".join(output)
with open(f"{current_year}.html", "w") as planner:
    planner.write(output)
