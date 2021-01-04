"""

"""

import os
import pickle
import sys

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Tuple

@dataclass
class WeekInfo:
    year: int
    week: int
    days: List[date] = field(default_factory=list)

week_by_date_maps: List[Dict[date, WeekInfo]] = ...
week_by_number_maps: List[Dict[Tuple[int, int], WeekInfo]] = ...

# Pickle file to cache table data generated in Excel
pickle_filename = 'table.pickle'

if os.path.exists(pickle_filename):
    with open(pickle_filename, 'rb') as f:
        week_by_date_maps, week_by_number_maps = pickle.load(f)

else:
    import xlwings as xw

    wb = xw.Book()
    wb.app.calculation = 'manual'

    sheet = wb.sheets.active

    # Populate formulas for a year
    for i in range(366):
        sheet[(i, 0)].value = '=DATE(2000,1,1)' if i == 0 else f'=A{i}+1'
        for j in range(7):
            sheet[(i, j + 1)].value = f'=WEEKNUM(A{i + 1}, {j + 11})'

    week_by_date_maps = [{} for _ in range(7)]
    week_by_number_maps = [{} for _ in range(7)]

    for year in range(1901, 2201):

        print(year, file=sys.stderr)

        sheet[(0, 0)].value = f'=DATE({year},1,1)'

        # Calculate WEEKNUM for all dates of a year
        wb.app.calculate()

        data = sheet.range((1, 1), (366, 8)).value

        # Remove extra day for non-leap years
        if data[-1][0].year != year:
            del data[-1]

        for day in data:

            dt = day[0].date()

            for i in range(7):
                w = int(day[1 + i])
                info = week_by_number_maps[i].get((dt.year, w))
                if info is None:
                    info = WeekInfo(year=dt.year, week=w)
                    week_by_number_maps[i][(dt.year, w)] = info
                info.days.append(dt)
                week_by_date_maps[i][dt] = info

    obj = (week_by_date_maps, week_by_number_maps)

    with open(pickle_filename, 'wb') as f:
        pickle.dump(obj, f)


from calweek import CalWeek, weeknum

def test():

    all_dates = list(sorted(week_by_date_maps[0].keys()))

    for i in range(7):
        for dt in all_dates:
            assert weeknum(dt, 11 + i) == week_by_date_maps[i][dt].week

    for dt in all_dates:
        assert week_by_date_maps[6][dt].week == CalWeek.withdate(dt).week

    for a in range(7):

        if a == 6:
            MyWeek = CalWeek
        else:
            class MyWeek(CalWeek):
                first_dow = a

        for y in range(1998, 2010):
            assert MyWeek.days_in_first_week(y) == len(week_by_number_maps[a][(y, 1)].days)

        w_prev = None

        checked = set()
        for dt in all_dates:

            w = MyWeek.withdate(dt)
            if w in checked:
                continue

            if w.week == 1 and w_prev is not None:
                assert w_prev == MyWeek.last_week_of_year(w_prev.year)

            w_prev = w

            checked.add(w)

            info = week_by_date_maps[a][dt]
            assert w.day(0) == info.days[0]

            assert w.days() == info.days


if __name__ == '__main__':
    test()
