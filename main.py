from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import datetime as dt
import calendar


def get_calendar() -> None:
    cal = calendar.month(year, month)
    days = []
    for i, row in enumerate(cal.splitlines()):
        if i in {0, 1}:
            continue
        days.append([date.zfill(2) for date in row.split()])

    while len(days[0]) != 7:
        days[0] = [" "] + days[0]
    while len(days[-1]) != 7:
        days[-1].append(" ")

    return days


def handler(event: Event) -> None:
    try:
        col = int(table.identify_column(event.x)[1])
        row = int(table.identify_row(event.y)[-1])
    except IndexError:
        return

    try:
        date = dt.date(year, month, int(get_calendar()[row-1][col-1]))
    except (TypeError, ValueError):
        return
    else:
        label2.config(text=f"{date.strftime('%A, %B %d, %Y')}".center(68))


def make_calendar(year: int, month: int) -> None:
    global table

    try:
        table.destroy()
    except NameError:
        pass

    label1.config(text=f"{MONTHS[month]}, {year}".center(80))

    days = get_calendar()
    table = ttk.Treeview(
        columns=tuple(range(7)), show="headings", height=len(days),
        selectmode="none"
    )
    table.bind('<Button-1>', handler)

    for i in range(7):
        table.heading(i, text=HEADINGS[i])
        table.column(i, minwidth=35, width=35)
    for row in days:
        table.insert("", "end", values=tuple(row))

    table.place(x=20, y=40)


def change(x: int) -> None:
    global year, month

    month += x
    if not month:
        year, month = year - 1, 12
    if month == 13:
        year, month = year + 1, 1

    make_calendar(year, month)


HEADINGS: list[str] = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
MONTHS: dict[int, str] = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "Spetember", 10: "October", 11: "November",
    12: "December",
}

root: Tk = Tk()
root.geometry("290x216")
root.title("Calendar")
root.resizable(False, False)

today: dt.datetime = dt.date.today()
month: int = today.month
year: int = today.year

label1: Label = Label(text=f"{MONTHS[today.month]}, {today.year}".center(80))
label1.place(x=10, y=10)

label2: Label = Label(text=f"{today.strftime('%A, %B %d, %Y')}".center(68))
label2.place(x=10, y=190)

Button(root, text=" < ", bd=2, command=(lambda: change(-1))).place(x=7, y=7)
Button(root, text=" > ", bd=2, command=(lambda: change(+1))).place(x=257, y=7)

make_calendar(year, month)

if __name__ == "__main__":
    root.mainloop()