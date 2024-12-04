#Functions
import json
import random
################Microservices###################################################

# Shuffle Cards
def microserviceA(my_input):

    def shuffle_norm(norm_list): # shuffles all cards in the list
        norm_list.pop(0) # remove the command
        val = []

        for x in range(len(norm_list)): # add all indexes to a list
            val.append(x) #

        random.shuffle(val) # shuffle list
        print(val)
        return val


    def shuffle_priority(all_cards): # shuffle only the high priority cards in the list
        all_cards.pop(0) # remove the command
        val = []
        val_index = 0

        for x in all_cards:
            if int(x) == 1: # add indexes of only priority cards
                val.append(val_index)
            val_index = val_index + 1 # track index

        random.shuffle(val) # shuffle the list of priority cards
        print(val)
        return val


    def shuffle_front(full_list):
        full_list.pop(0) # remove command
        priority = []
        reg = []
        val_index = 0
        for x in full_list:
            if int(x) == 1: # add just priority
                priority.append(val_index)
            else:
                reg.append(val_index) # otherwise non priority
            val_index = val_index + 1

        # shuffle both independently
        random.shuffle(reg)
        random.shuffle(priority)

        all_shuffled = priority + reg # add priority before non priority

        print(all_shuffled)
        return all_shuffled


    def create_list(cards): # decodes and reformat all string values sent by client
        c_list = cards.decode().split(",")
        return c_list


    def string_output(list_output): # reformat the lists into strings as tokens separated by ","

        str_output = ""
        count = 0
        for x in list_output:
            if count != len(list_output) - 1: # if catches commas from being added to the end
                str_output = str_output + str(x) + ","
            else:
                str_output = str_output + str(x)
            count = count + 1
        return str_output



    # VALID EXAMPLE STRING FROM CLIENT: R,1,1,1,0,0,1,1,0,1

    while True:

        cards_to_shuffle = my_input

        if len(cards_to_shuffle) > 0:
            card_list = my_input
            output = ""

            if card_list[0] == 'R': # R command for shuffle normal
                output = shuffle_norm(card_list)

            if card_list[0] == 'P': # P command for shuffling all non priority
                output = shuffle_priority(card_list)

            if card_list[0] == 'F': # F command for shuffling both but front loading with priority
                output = shuffle_front(card_list)

            if input == "Q":
                break

            if output == "": # if input does not contain any commands
                output = "invalid"
            else:
                output = string_output(output)


    return output

# Load to/from File
def microserviceB(my_input):

    # Input : 
    # Load Bit + Deck Name + "***" + File path
    load_bit = my_input[0]

    deck_name, filepath = my_input[1:].split("***")

    # Load bit = 0, load from file
    # Load bit = 1, load to file
    if load_bit == "0":
        file = open(filepath, "r")

        my_data = {}

        for ln in file:
            frontback = ln.split(' / ')
            back = frontback[1].split('\n')
            my_data[frontback[0]] = [back[0], 0]

        file.close()

        with open("data2.json", "r") as f:
            my_list = json.load(f)

        new_position = str(len(my_list) + 1)

        name_of_deck = deck_name

        my_list[new_position] = [my_data, name_of_deck]

        with open("data2.json", "w") as f:
            json.dump(my_list, f)
    else:
        # Load to file
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

# Reverse
def microserviceC(my_input):

    deck_place = my_input[0] # Provide which deck we're loading in
    new_deck = {}

    with open("data2.json", "r") as f:
        my_list = json.load(f)

    f.close()

    # deck_place = "1"
    old_deck = my_list[deck_place][0]

    for i in old_deck:
        new_deck[old_deck[i][0]] = [i,old_deck[i][1]]

    my_list[deck_place][0] = new_deck

    with open("data2.json", "w") as f:
        json.dump(my_list, f)

# Wipe priorities
def microserviceD(my_input):
    # index 0: index in json
    # index 1: Load bit - D for wipe, U for Undo
    with open("data2.json", "r") as f:
        my_list = json.load(f)

    f.close()

    my_place = my_input[0]

    load_bit = my_input[1]

    if load_bit == "D":
        local_deck = my_list[my_place][0]

        old_stuff = {"OLD": local_deck}

        with open("oldstuff.json", "w") as f:
            json.dump(old_stuff, f)
        
        f.close()

        for i in local_deck:
            local_deck[i][1] = 0

    if load_bit == "U":
        with open("oldstuff.json", "r") as f:
            local_deck = json.load(f)
        f.close()

    my_list[my_place] = local_deck

    with open("data2.json", "w") as f:
        json.dump(my_list, f)





################################################################################

def welcomeScreen():
    print("")
    print("Welcome to the Card App!")
    print("")
    print("Menu:")
    print("     1. Go to all decks!")
    print("     2. Go to my favorite decks!")
    print("     3. Help page")
    pageInput = input("Enter: ")
    print("")
    if pageInput == "":
        return ""
    return int(pageInput)

def favoriteDeck(my_deck,directory,current_position):
    if directory[current_position][2] == 1:
        directory[current_position][2] = 0
    else:
        directory[current_position][2] = 1
    with open("data2.json", "w") as f:
        json.dump(directory, f)

def prioritizeCards(my_deck,directory,current_position):
    print("List of current Cards: ")

    for i in my_deck:
        if my_deck[i][1] == 1:
            print(i + " / " + my_deck[i][0] + " - High Priority")
        else:
            print(i + " / " + my_deck[i][0] + " - Low Priority")

    print("Switch a card's Priority by typing the name on the front of the card.")
    my_card = input("Enter: ")
    if my_deck[my_card][1] == 1:
        my_deck[my_card][1] = 0
    else:
        my_deck[my_card][1] = 1
    directory[current_position][0] = my_deck
    with open("data2.json", "w") as f:
        json.dump(directory, f)

def loadFromDeck(directory, new_position,name_of_deck):
    name_of_file = input("What is the name of your file? ")
    my_data = "0" + name_of_deck + "***" + name_of_file
    microserviceB(my_data)

def makeNewDeck(directory):
    new_position = str(len(directory) + 1)
    yesNo = input("Want to load a new deck from a file? ")
    if yesNo == "Y":
        name_of_deck = input("What do you want your deck to be called? ")
        loadFromDeck(directory, new_position, name_of_deck)

    else:
        name_of_deck = input("What do you want your deck to be called? ")
        if name_of_deck != '':
            directory[new_position] = [{}, name_of_deck]
            with open("data2.json", "w") as f:
                json.dump(directory, f)

def deleteDeck(directory,current_position):
    print("Are you sure you want to permamnently delete this deck? This action cannot be undone.")
    yn = input("(Y)es or (N)o: ").upper()
    print("")
    if yn == "Y":
        del directory[current_position]
        with open("data2.json", "w") as f:
            json.dump(directory, f)


def addCards(my_deck,directory,current_position):
    front = input("Front: ")
    back = input("Back: ")
    my_deck[front] = [back, 0]
    directory[current_position][0] = my_deck
    with open("data2.json", "w") as f:
        json.dump(directory, f)
    return my_deck

def deleteCards(my_deck,directory,current_position):
    to_delete = input("Select a card to delete: ")
    if to_delete not in my_deck:
        print("That card was not found.")
        return my_deck
    are_you_sure = input("Are you sure you want to delete this card? (Y/N): ").upper()

    if are_you_sure == "Y":
        del my_deck[to_delete]
    directory[current_position][0] = my_deck
    with open("data2.json", "w") as f:
        json.dump(directory, f)
    return my_deck


def showAnswer(local_list, current_loc):
    current_card = local_list[current_loc]
    back_of_card = current_card[1]
    print(back_of_card)
    b = input("(B)ack to front of Card: ").upper()
    if b == "B":
        my_thing = 1

def highPriorityBuilder(my_deck):
    print("Want to study all cards, or only high priority cards?")
    answer = input("(A)ll Cards, (H)igh Priority: ").upper()
    if answer == 'A':
        return my_deck
    if answer == 'H':
        new_deck = {}
        for i in my_deck:
            if my_deck[i][1] == 1:
                new_deck[i] = [my_deck[i][0], 0]
        return new_deck
    return my_deck

def studyDeck(my_deck):
    all_deck = my_deck
    my_deck = highPriorityBuilder(my_deck)
    length = len(my_deck)
    current_loc = 0
    visited = [i for i in range(1,length)]
    keep_going = True
    local_list = list(my_deck.items())
    last_lap = False

    while keep_going == True:
        print("Front: " + local_list[current_loc][0])
        option = input("(A)nswer, (L)eft, (R)ight: ").upper()
        if option == "R":
            current_loc += 1
            if current_loc == length:
                current_loc = 0
        if option == "L":
            current_loc -= 1
            if current_loc == -1:
                current_loc = length - 1
        if option == "A":
            showAnswer(local_list, current_loc)

        if current_loc in visited:
            visited.remove(current_loc)


        if (last_lap == True) or (option == ''):
            keep_going = False

        if visited == []:
            last_lap = True
    
    print("You've reached the end of the deck!")
    go_again = input("Go again? (Y/N): ").upper()
    print("")
    if go_again == "Y":
        studyDeck(all_deck)
    else:
        no = "NO"

def showAnswer(local_list, current_loc):
    current_card = local_list[current_loc]
    back_of_card = current_card[1][0]
    print(back_of_card)
    b = input("(R)eturn to front of Card: ").upper()
    if b == "R":
        my_thing = 1


def examineDeck(my_deck):
    for i in my_deck:
        if my_deck[i][1] == 1:
            print(i + " / " + my_deck[i][0] + " - High Priority")
        else:
            print(i + " / " + my_deck[i][0])
    print("")

def shuffleCards(my_deck, directory, current_position):
    all_or_high = input("Want to shuffle all cards, or just high priority ones?")
    if all_or_high == "ALL":
        load_bit = "R"
    else:
        load_bit = "P"

    #my_list = [4,2,6,1]

    new_dict = {}

    my_deck_keys = my_deck.keys()
    my_deck_values = my_deck.values()

    priorities = [load_bit]

    for thing in my_deck_values:
        priorities.append(thing[1])

    my_list = microserviceA(priorities)
    

    local_index = 0

    if load_bit == "R":
        while len(my_deck_keys) > 0:

            for number in my_list:
                if number == local_index:
                    local_key = my_deck_keys.pop(local_index)
                    local_value = my_deck_values.pop(local_index)

                    new_dict[local_key] = local_value

            local_index += 1

    if load_bit == "P":
        while local_index <= len(my_list):

            for number in my_list:
                if number == local_index:
                    local_key = my_deck_keys.pop(local_index)
                    local_value = my_deck_values.pop(local_index)

                    new_dict[local_key] = local_value

            local_index += 1


    directory[current_position][0] = new_dict
    with open("data2.json", "w") as f:
        json.dump(directory, f)

def saveToFile(my_deck, directory, current_position):
    load_bit = "0"

    name_of_deck = input("Name of the deck we want to load? ")
    filepath = input("Filepath of the text file?")
    microservice_input = load_bit + name_of_deck + "***" + filepath

    microserviceB(microservice_input)

def reverseAllCards(directory):
    length = len(directory)
    my_positions = [str(i) for i in range(1,length + 1)]

    for j in my_positions:
        microserviceC(j)

def reverseCards(my_deck, directory, current_position):
    all_cards = input("Want to reverse all decks? ")
    if all_cards == "Y":
        reverseAllCards(directory)

    else:
        microserviceC(str(current_position))


def dePrioritize(my_deck, directory, current_position):
    my_input = str(current_position) + "D"
    microserviceD(my_input)

def loadPriorities(my_deck, directory, current_position):
    my_input = str(current_position) + "U"
    microserviceD(my_input)

def singleDeckPage(my_deck,directory,current_position):
    print("Make your selection:")
    print("     1. Add Cards")
    print("     2. Delete Cards")
    print("     3. Study Deck")
    print("     4. Examine Deck")
    print("     5. Prioritize Cards")
    if directory[current_position][2] == 0:
        print("     6. Favorite this Deck")
    else:
        print("     6. Un-Favorite this Deck")
    print("     7. Delete Entire Deck")
    print("     8. Shuffle Cards")
    print("     9. Save to File")
    print("     10. Reverse Sides of Cards")
    print("     11. De-Prioritize All Cards")
    print("     12. Load Previous Priorities")
    myChoice = input("Enter: ")
    print("")
    if myChoice != "":
        myChoice = int(myChoice)
    if myChoice == 1:
        my_deck = addCards(my_deck,directory,current_position)
    if myChoice == 2:
        my_deck = deleteCards(my_deck,directory,current_position)
    if myChoice == 3:
        studyDeck(my_deck)
    if myChoice == 4:
        examineDeck(my_deck)
    if myChoice == 5:
        prioritizeCards(my_deck,directory,current_position)
    if myChoice == 6:
        favoriteDeck(my_deck,directory,current_position)
    if myChoice == 7:
        deleteDeck(my_deck, directory, current_position)
    if myChoice == 8:
        shuffleCards(my_deck, directory, current_position)
    if myChoice == 9:
        saveToFile(my_deck, directory, current_position)
    if myChoice == 10:
        reverseCards(my_deck, directory, current_position)
    if myChoice == 11:
        dePrioritize(my_deck, directory, current_position)
    if myChoice == 12:
        loadPriorities(my_deck, directory, current_position)


def deckDirectory(number):
    mountains = {"Mount Everest": ["Nepal", 0], "K2": ["Pakistan", 1], "Kangchenjunga": ["India", 0], "Gangkhar Puensum": ["Bhutan", 1]}
    books = {"Catcher in the Rye": ["J.D. Salinger", 1], "Turn of the Screw": ["Henry James", 0], "Oliver Twist": ["Charles Dickens", 1], "Moby Dick": ["Herman Melville", 0]}
    arts = {"Mona Lisa": ["Da Vinci", 0], "The Birth of Venus": ["Botticelli", 1], "Dog Barking at the Moon": ["Joan Miro", 0], "Persistence of Memory": ["Salvador Dali", 0]}
    my_list = {1: [mountains, "Mountains"], 2: [books, "Books"], 3: [arts, "Arts"]}
    my_deck = my_list[number]
    singleDeckPage(my_deck)

def getDeckData():
    with open("data2.json", "r") as f:
        my_list = json.load(f)
    print("Select Your Deck!")
    for i in range(1,len(my_list)+1):
        if my_list[str(i)][2] == 1:
            print("     " + str(i) + ". " + my_list[str(i)][1] + " - " + str(len(my_list[str(i)][0])) + " cards - *")
        else:
            print("     " + str(i) + ". " + my_list[str(i)][1] + " - " + str(len(my_list[str(i)][0])) + " cards")
    print("     " + str(i+1) + ". Make a New Deck!")
    
    goToDeck = input("Enter your deck: ")
    print("")
    if goToDeck != '':
        if int(goToDeck) == i+1:
            makeNewDeck(my_list)
        else:
            if goToDeck != '':
                #goToDeck = int(goToDeck)
                singleDeckPage(my_list[goToDeck][0],my_list,goToDeck)
            else:
                return goToDeck    
    else:
        return goToDeck

def getDeckDataFavoritesOnly():
    with open("data2.json", "r") as f:
        my_list = json.load(f)
    print("Select Your Deck!")
    index_mapping = {}
    local_count = 1
    for i in range(1,len(my_list)+1):
        if my_list[str(i)][2] == 1:
            index_mapping[local_count] = i
            print("     " + str(local_count) + ". " + my_list[str(i)][1] + " - " + str(len(my_list[str(i)][0])) + " cards - *")
            local_count += 1
    print("     " + str(local_count) + ". Make a New Deck!")
    
    goToDeck = input("Enter your deck: ")
    print("")
    if goToDeck != '':
        if int(goToDeck) == (local_count+1):
            makeNewDeck(my_list)
        else:
            if goToDeck != '':
                #goToDeck = int(goToDeck)
                real_position = str(index_mapping[int(goToDeck)])
                singleDeckPage(my_list[real_position][0],my_list,real_position)
            else:
                return goToDeck    
    else:
        return goToDeck


def deckPage():
    return getDeckData()
    '''
    print("Select your Deck!")
    print("     1. Mountains")
    print("     2. Books")
    print("     3. Arts")
    goToDeck = input("Enter your deck: ")
    if goToDeck != '':
        deckDirectory(int(goToDeck))
    else:
        return goToDeck
    '''

def helpPage():
    print("The purpose of this application is to provide users with a program to learn and review content on flashcards.")
    print("")
    print("     1. Managing Your Decks")
    print("         a. Decks may be created, added to, or subtracted from in order to suit your needs. ")
    print("         b. You may also delete a deck entirely, though be warned that this is a permanent ")
    print("            deletion, and you will not be able to retrieve your data afterwords.")
    print("         c. You may favorite or un-favorite decks. Your favorite decks will appear with an ")
    print("            asterisk after them in your listing of decks. You will have the option to only view")
    print("            your favorite decks.")
    print("")
    print("     2. Studying from Your Decks")
    print("         a. You may iterate through the cards in your deck, in either the left or right direction. ")
    print("         a. Once you reach the end of your deck, you will receive an alert telling you that  ")
    print("            you’ve iterated through all of your cards.")
    print("         b. You may mark specific cards as high-priority, and choose to only iterate through   ")
    print("            those cards as needed.  ")


if __name__ == '__main__':
    
    quit_var = False
    while quit_var == False:
        study_decks = True
        my_selection = welcomeScreen()
        if my_selection == 1:
            while study_decks == True:
                blanker = deckPage()
                if blanker == '':
                    study_decks = False

        else:
            if my_selection == 2:
                getDeckDataFavoritesOnly()
            else:
                if my_selection == 3:
                    helpPage()
                else:
                    quit_var = True
