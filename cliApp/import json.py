import json


with open("data2.json", "r") as f:
    my_stuff = json.load(f)

for i in my_stuff:
    print(i)