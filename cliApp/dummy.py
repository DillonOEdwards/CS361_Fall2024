import json

mountains = {"Mount Everest": ["Nepal", 0], "K2": ["Pakistan", 1], "Kangchenjunga": ["India", 0], "Gangkhar Puensum": ["Bhutan", 1]}
books = {"Catcher in the Rye": ["J.D. Salinger", 1], "Turn of the Screw": ["Henry James", 0], "Oliver Twist": ["Charles Dickens", 1], "Moby Dick": ["Herman Melville", 0]}
arts = {"Mona Lisa": ["Da Vinci", 0], "The Birth of Venus": ["Botticelli", 1], "Dog Barking at the Moon": ["Joan Miro", 0], "Persistence of Memory": ["Salvador Dali", 0]}
my_list = {1: [mountains, "Mountains", 0], 2: [books, "Books"], 3: [arts, "Arts"]}

with open("data5.json", "w") as f:
    json.dump(my_list, f)




