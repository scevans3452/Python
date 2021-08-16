# try:
number = input("Please enter a number:")

# if number != int or float:
#     raise Exception("The value entered was not a number. Please enter numerical digits ONLY.")
# else:
#     pass

x = int(number) % 2

if x == 0:
    print("Your number is even")
else:
    print("Your number is odd")

# except Exception("You didn't put a number...")