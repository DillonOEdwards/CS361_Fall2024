## De-prioritize Cards

import json

with open("data2.json", "r") as f:
    my_list = json.load(f)

f.close()

my_place = "1"

local_deck = my_list[my_place][0]

old_places = []

for i in local_deck:
    old_places.append(local_deck[i][1])
    local_deck[i][1] = 0

textfile = "oldvalues" + my_list[my_place][1] + ".txt"

file = open(textfile, "x")

for i in old_places:
    file.write(i)

file.close()