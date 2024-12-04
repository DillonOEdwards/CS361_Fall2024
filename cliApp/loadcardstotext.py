# Load cards to text file

import json

with open("data2.json", "r") as f:
    my_list = json.load(f)

my_deck_num = "1"
my_textfile = "mountainsave.txt"

file = open(my_textfile, "x")

my_deck = my_list[my_deck_num][0]

for i in my_deck:
    new_string = i + " / " + my_deck[i][0]
    file.write(new_string)

file.close()