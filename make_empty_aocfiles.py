from __future__ import annotations

from pathlib import Path

year: int = 2021
dayprefix: str = 'day'

rootdir = Path(__file__).parent

if not (yeardir := Path(rootdir, str(year))).exists():
    yeardir.mkdir(parents=True)

for dayno in range(1, 26):
    if not (daydir := Path(yeardir, f'{dayprefix}{dayno}')).exists():
        daydir.mkdir(parents=True)


    if not (pyfilepath := Path(daydir, f"{dayprefix}{dayno}").with_suffix('.py')).exists():
        with open(pyfilepath, 'w') as pyfile:
            pyfile.write('\n')

    for inputkind in ('-example', ''):
        if not (inputfilepath := Path(daydir, f"input{dayno}{inputkind}").with_suffix('.txt')).exists():
            with open(inputfilepath, 'w') as txtinputfile:
                txtinputfile.write('\n')
