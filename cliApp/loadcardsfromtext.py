# Make cards from Text file
import json

file = open("cliApp/worldleaders.txt", "r")

my_data = {}

for ln in file:
    frontback = ln.split(' / ')
    back = frontback[1].split('\n')
    my_data[frontback[0]] = [back[0], 0]

file.close()

with open("data2.json", "r") as f:
    my_list = json.load(f)

new_position = str(len(my_list) + 1)

name_of_deck = "World Leaders"

my_list[new_position] = [my_data, name_of_deck]

with open("data2.json", "w") as f:
    json.dump(my_list, f)