import string
a = "Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient python, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, baxa quouq. axa la consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Proin at neque et tellus ultricies consequat. Duis vitae mi commodo, suscipit nunc vel, porta tellus. In eu volutpat sapien. Mauris dignissim velit eget diam tristique, nec egestas magna maximus. Pellentesque python, lorem a eleifend vehicula, arcu urna facilisis odio, maximus maximus massa nisl sed sapien. Quisque nisi nunc, dignissim ut malesuada non, fringilla vitae sem. Nunc turpis quam, rutrum at egestas ut, pretium tincidunt est. Praesent imperdiet mauris eu felis lobortis vehicula. Sed dictum lorem at rutrum rhoncus. Suspendisse sit amet ex ac eros python cursus. Duis pretium rutrum lacus, sit amet vulputate ipsum condimentum vel. Vivamus lacus ipsum, python in justo quis, blandit condimentum velit esed semper posuere leo, elementum tristique leo euismod quis."

commas = 0
periods = 0 #find the number of commas and periods that occur after words with exactly four letters.
# com_literal = ""
# per_literal = ""
asc = string.ascii_lowercase
b = a.split(" ")
d = ""


for i in b:
    if i.endswith(",") and (len(i) == 5):
        commas += 1
        # com_literal += i
    elif i.endswith(".") and (len(i) == 5):
        periods += 1
        # per_literal += i

total = str(commas + periods)
print("The total is " + total)

for x in total:
    d += asc[int(x)]

txt = "The cypher is {}"

print(txt.format(d))
# print(commas)
# print(com_literal)
# print(periods)
# print(per_literal)
# print(b)