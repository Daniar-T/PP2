# 1. Write a Python program to subtract five days from current date.

from datetime import date, timedelta

current_date = date.today()
five_days_ago = current_date - timedelta(days=5)

print(five_days_ago)

# 2. Write a Python program to print yesterday, today, tomorrow.

from datetime import date, timedelta

today = date.today()

print("Yesterday:", today - timedelta(days=1))
print("Today:", today)
print("Tomorrow:", today + timedelta(days=1))

#3. Write a Python program to drop microseconds from datetime.

from datetime import datetime

now = datetime.now()
without_microseconds = now.replace(microsecond=0)

print(without_microseconds)

#4. Write a Python program to calculate two date difference in seconds.

from datetime import datetime

date_1 = datetime(2024, 5, 17, 10, 0, 0)
date_2 = datetime(2024, 5, 17, 12, 30, 0)

difference = date_2 - date_1

print(difference.total_seconds())