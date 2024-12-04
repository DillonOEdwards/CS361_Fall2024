print("My Decks:")

deck = open("/mountains.txt", "r")

decktitle = deck.readline()
print(decktitle)

while True:
    card = deck.readline()
    if not card:
        break
    print(card)

deck.close()