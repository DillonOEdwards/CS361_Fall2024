## Reverse sides of cards

import json

new_deck = {}

with open("data2.json", "r") as f:
    my_list = json.load(f)

f.close()

deck_place = "1"
old_deck = my_list[deck_place][0]

for i in old_deck:
    new_deck[old_deck[i][0]] = [i,old_deck[i][1]]

my_list[deck_place][0] = new_deck

with open("data2.json", "w") as f:
    json.dump(my_list, f)