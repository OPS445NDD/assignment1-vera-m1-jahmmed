import sys

def leap_year(year: int) -> bool:
    '''
    leap_year() -> bool
    Returns True if the given year is a leap year, False otherwise.
    '''
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False

def mon_max(month: int, year: int) -> int:
    '''
    mon_max(month, year) -> int
    Returns the maximum number of days in the given month of the given year.
    '''
    if leap_year(year):
        feb_max = 29
    else:
        feb_max = 28

    month_days = { 1:31, 2:feb_max, 3:31, 4:30, 5:31, 6:30,
                   7:31, 8:31, 9:30, 10:31, 11:30, 12:31 }

    return month_days[month]

def after(date: str) -> str:
    '''
    after() -> date for next day in YYYY-MM-DD string format

    Return the date for the next day of the given date in YYYY-MM-DD format.
    This function takes care of the number of days in February for leap year.
    This function has been tested to work for year after 1582
    '''
    str_year, str_month, str_day = date.split('-')  # Split the date string into year, month, day parts
    year = int(str_year)    # Convert year string to integer
    month = int(str_month)  # Convert month string to integer
    day = int(str_day)      # Convert day string to integer

    tmp_day = day + 1  # Calculate the next day by adding 1

    if tmp_day > mon_max(month, year):           # If next day exceeds this month's max days
        to_day = tmp_day % mon_max(month, year)  # Wrap around to day 1 of next month
        tmp_month = month + 1                    # Move to the next month
    else:
        to_day = tmp_day   # Day is valid, keep it
        tmp_month = month  # Month stays the same

    if tmp_month > 12:   # If month goes past December
        to_month = 1     # Wrap around to January
        year = year + 1  # Increment the year
    else:
        to_month = tmp_month  # Month is valid, keep it

    next_date = f"{year}-{to_month:02}-{to_day:02}"  # Format as YYYY-MM-DD with zero padding

    return next_date  # Return the next day's date


if __name__ == "__main__":
    # Test after()
    print(after('2023-01-25'))   # Expected: 2023-01-26
    print(after('2016-02-28'))   # Expected: 2016-02-29
    print(after('2025-12-31'))   # Expected: 2026-01-01

    # Test leap_year()
    print(leap_year(2000))  # Expected: True
    print(leap_year(1900))  # Expected: False
    print(leap_year(2024))  # Expected: True
    print(leap_year(2023))  # Expected: False

    # Test mon_max()
    print(mon_max(2, 2024))  # Expected: 29
    print(mon_max(2, 2023))  # Expected: 28
    print(mon_max(1, 2023))  # Expected: 31

def day_of_week(date: str) -> str:
    '''
    Returns the day of the week for a given date in YYYY-MM-DD format.
    Returns one of: 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'
    '''
    day, month, year = (int(x) for x in date.split('-')[::-1])
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    offset = {1:0, 2:3, 3:2, 4:5, 5:0, 6:3, 7:5, 8:1, 9:4, 10:6, 11:2, 12:4}
    if month < 3:
        year -= 1
    num = (year + year//4 - year//100 + year//400 + offset[month] + day) % 7
    return days[num]


def valid_date(date: str) -> bool:
    '''
    valid_date(date) -> True or False

    Checks if a given date string in YYYY-MM-DD format is a valid calendar date.
    Returns True if valid, False if not.

    Checks performed:
    - String must be in YYYY-MM-DD format
    - Month must be between 1 and 12
    - Day must be valid for the given month and year (handles leap years)
    '''
    # Step 4a: Make sure the format is correct using split
    parts = date.split('-')

    if len(parts) != 3:
        return False   # must have exactly 3 parts: year, month, day

    str_year, str_month, str_day = parts

    # Step 4b: Make sure all parts are numeric digits only
    if not str_year.isdigit() or not str_month.isdigit() or not str_day.isdigit():
        return False   # non-numeric characters found

    year = int(str_year)
    month = int(str_month)
    day = int(str_day)

    # Step 4c: Check month is within valid range
    if month < 1 or month > 12:
        return False   # month must be 1-12

    # Step 4d: Check day is within valid range for that month/year
    if day < 1 or day > mon_max(month, year):
        return False   # day out of range for this month

    return True   # all checks passed - date is valid


def day_count(start_date: str, end_date: str) -> int:
    '''
    day_count(start_date, end_date) -> int

    Counts and returns the number of weekend days (Saturdays and Sundays)
    between start_date and end_date, inclusive of both dates.

    Both dates should be in YYYY-MM-DD format.
    start_date must be earlier than or equal to end_date.
    '''
    weekend_count = 0          # counter for weekend days
    current_date = start_date  # begin at the start date

    # Loop from start_date up to AND including end_date
    while current_date <= end_date:

        # Get the day of week for the current date
        day = day_of_week(current_date)

        # Check if it's a Saturday or Sunday
        if day == 'sat' or day == 'sun':
            weekend_count += 1   # increment weekend counter

        # Move to the next day using after()
        current_date = after(current_date)

    return weekend_count   # return total weekend days found

if __name__ == "__main__":
    # Quick test of valid_date
    print(valid_date('2023-05-01'))   # should print True
    print(valid_date('2023-13-01'))   # should print False (bad month)
    print(valid_date('2023-02-30'))   # should print False (bad day)

    # Quick test of day_count
    print(day_count('2023-05-01', '2023-05-30'))  # should print 8
