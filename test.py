import random

MIDDLE_OF_DECK = 26

def array_to_bytestring(input_array):
    output_str = ""
    for each in input_array:
        output_str = output_str + " " + each
    return output_str.encode()


def creat_cards():
    deck = []
    i = 0
    while i < 52:
        deck.append(str(i))
        i = i + 1
    random.shuffle(deck)

    return deck[MIDDLE_OF_DECK:], deck[:MIDDLE_OF_DECK]

deck1, deck2 = creat_cards()
print(len(deck1))
print(array_to_bytestring(deck1))
print(len(deck2))
print(array_to_bytestring(deck2))
