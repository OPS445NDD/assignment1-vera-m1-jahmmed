#!/usr/bin/env python3
'''
OPS445 Assignment 1
Program: assignment1.py
Author: Jahid Ahmed
Seneca Username: jahmmed
Date: 2025

I confirm that the work contained in this assignment is my own,
except where clearly indicated. I have received, and I understand,
the course guidelines on academic integrity.
'''

import sys


def leap_year(year: int) -> bool:
    '''
    leap_year(year) -> bool

    Returns True if the given year is a leap year, False otherwise.
    Leap year rules:
    - Divisible by 400 = leap year
    - Divisible by 100 but not 400 = not leap year
    - Divisible by 4 but not 100 = leap year
    - Everything else = not leap year
    '''
    if year % 400 == 0:
        return True   # divisible by 400 is always a leap year
    if year % 100 == 0:
        return False  # divisible by 100 but not 400 is not a leap year
    if year % 4 == 0:
        return True   # divisible by 4 but not 100 is a leap year
    return False      # all other years are not leap years


def mon_max(month: int, year: int) -> int:
    '''
    mon_max(month, year) -> int

    Returns the maximum number of days in the given month of the given year.
    Accounts for leap years when calculating February's max days.
    '''
    feb_max = 29 if leap_year(year) else 28  # February depends on leap year

    # map each month number to its maximum days
    month_days = {
        1: 31, 2: feb_max, 3: 31, 4: 30,
        5: 31, 6: 30,      7: 31, 8: 31,
        9: 30, 10: 31,    11: 30, 12: 31
    }
    return month_days[month]


def after(date: str) -> str:
    '''
    after() -> date for next day in YYYY-MM-DD string format

    Return the date for the next day of the given date in YYYY-MM-DD format.
    This function takes care of the number of days in February for leap year.
    This function has been tested to work for year after 1582.
    '''
    str_year, str_month, str_day = date.split('-')  # split into 3 parts
    year = int(str_year)    # convert year to integer
    month = int(str_month)  # convert month to integer
    day = int(str_day)      # convert day to integer

    tmp_day = day + 1  # move to next day

    if tmp_day > mon_max(month, year):           # if next day exceeds month max
        to_day = tmp_day % mon_max(month, year)  # wrap to day 1 of next month
        tmp_month = month + 1                    # advance to next month
    else:
        to_day = tmp_day   # day is still valid in this month
        tmp_month = month  # month stays the same

    if tmp_month > 12:    # if month goes past December
        to_month = 1      # wrap back to January
        year = year + 1   # and increment the year
    else:
        to_month = tmp_month  # month is valid, keep it

    next_date = f"{year}-{to_month:02}-{to_day:02}"  # format as YYYY-MM-DD
    return next_date


def day_of_week(date: str) -> str:
    '''
    day_of_week(date) -> str

    Returns the day of the week for a given date in YYYY-MM-DD format.
    Returns one of: 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'
    Uses the Tomohiko Sakamoto algorithm to calculate the day.
    '''
    day, month, year = (int(x) for x in date.split('-')[::-1])
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    offset = {1:0, 2:3, 3:2, 4:5, 5:0, 6:3, 7:5, 8:1, 9:4, 10:6, 11:2, 12:4}
    if month < 3:
        year -= 1  # adjust year for January and February
    num = (year + year//4 - year//100 + year//400 + offset[month] + day) % 7
    return days[num]


def valid_date(date: str) -> bool:
    '''
    valid_date(date) -> bool

    Checks if a given date string in YYYY-MM-DD format is a valid calendar date.
    Returns True if valid, False if not.

    Checks performed:
    - String must split into exactly 3 parts separated by '-'
    - All 3 parts must be numeric
    - Month must be between 1 and 12
    - Day must be valid for the given month and year (handles leap years)
    '''
    parts = date.split('-')

    if len(parts) != 3:
        return False  # must have exactly year, month, day parts

    str_year, str_month, str_day = parts

    # all parts must contain only digits
    if not str_year.isdigit() or not str_month.isdigit() or not str_day.isdigit():
        return False  # non-numeric value found

    year = int(str_year)
    month = int(str_month)
    day = int(str_day)

    # month must be between 1 and 12 inclusive
    if month < 1 or month > 12:
        return False  # invalid month number

    # day must be between 1 and max days for that month/year
    if day < 1 or day > mon_max(month, year):
        return False  # invalid day for this month

    return True  # all checks passed, date is valid


def day_count(start_date: str, end_date: str) -> int:
    '''
    day_count(start_date, end_date) -> int

    Counts and returns the number of weekend days (Saturdays and Sundays)
    between start_date and end_date, inclusive of both dates.

    Both dates must be in YYYY-MM-DD format.
    start_date must be earlier than or equal to end_date to avoid infinite loop.
    '''
    weekend_count = 0          # tracks total number of weekend days found
    current_date = start_date  # start iterating from the start date

    # loop through every day from start to end, inclusive
    while current_date <= end_date:

        day = day_of_week(current_date)  # get the weekday name for current date

        if day == 'sat' or day == 'sun':
            weekend_count += 1  # count it if Saturday or Sunday

        current_date = after(current_date)  # move to the next day

    return weekend_count  # return total weekend days counted


def usage():
    '''
    usage() -> None

    Prints a helpful usage message to the user and exits the program.
    Called when the user provides invalid arguments.
    '''
    print("Usage: assignment1.py YYYY-MM-DD YYYY-MM-DD")
    print("Please provide two valid dates in YYYY-MM-DD format.")
    sys.exit(1)


if __name__ == "__main__":

    # check that exactly 2 arguments were provided
    if len(sys.argv) != 3:
        usage()

    date1 = sys.argv[1]  # first date argument from command line
    date2 = sys.argv[2]  # second date argument from command line

    # validate both dates before using them
    if not valid_date(date1) or not valid_date(date2):
        usage()

    # ensure start_date is always the earlier date
    if date1 <= date2:
        start_date = date1
        end_date = date2
    else:
        start_date = date2  # swap if user entered dates in wrong order
        end_date = date1

    # calculate and print the number of weekend days
    count = day_count(start_date, end_date)
    print(f"The period between {start_date} and {end_date} includes {count} weekend days.")
