import datetime
import string

old_time = datetime.datetime(1892, 11, 24)
new_time = datetime.datetime(2000, 1, 1)


days = str(new_time - old_time)
days = days[0:5]
txt = string.ascii_lowercase

answer = ""


for i in days:
    print(i)
    answer += txt[int(i)]


txt = "The cypher is {}"
print(txt.format(answer))

# year = new_time.year - old_time.year
# print(year)

# month = new_time.month - old_time.month
# print(month)

# day = new_time.day - old_time.day
# print(day)