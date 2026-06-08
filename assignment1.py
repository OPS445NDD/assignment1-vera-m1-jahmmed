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
