"""
Kevin Monahan
CompSci 520 - Homework 3
10/30/2023
War Server
"""
import random
import socket
import sys

PORT = 4444
WANT_GAME = b'\x00'
GAME_START = b'\x01'
PLAY_CARD = b'\x02'
PLAY_RESULT = b'\x03'
WIN = b'\x00'
DRAW = b'\x01'
LOSE = b'\x02'
RESPONSE_LENGTH = 1
MIDDLE_OF_DECK = 26
CARDS_TO_SUIT = 13


def array_to_bytestring(input_array):
    """Converts an input array of strings into a bytestring"""
    output_str = b''
    for each in input_array:
        output_str = output_str + each
    return output_str


def creat_cards():
    """Creates two hands of 26 cards each returned as a tuple of bytestrings"""
    deck = []
    i = 0
    while i < 52:
        deck.append(i.to_bytes(1, "little"))
        i = i + 1
    random.shuffle(deck)
    deck1 = array_to_bytestring(deck[MIDDLE_OF_DECK:])
    deck2 = array_to_bytestring(deck[:MIDDLE_OF_DECK])
    return deck1, deck2


def start_game(client1, client2):
    """Starts the game between two clients sending each 26 cards"""
    deck1, deck2 = creat_cards()
    client1.send(GAME_START + deck1)
    client2.send(GAME_START + deck2)


def parse_card(card_byte):
    """Takes in a byte and returns the integer value of that byte"""
    return int.from_bytes(card_byte, "little")


def compare_cards(card1, card2, client1, client2):
    """Compares two cards and based on their values
    returns win, loss, or draw to each client"""
    card1 = card1 % CARDS_TO_SUIT
    card2 = card2 % CARDS_TO_SUIT
    if card1 > card2:
        client1.send(PLAY_RESULT + WIN)
        client2.send(PLAY_RESULT + LOSE)
        return
    if card1 == card2:
        client1.send(PLAY_RESULT + DRAW)
        client2.send(PLAY_RESULT + DRAW)
        return
    client1.send(PLAY_RESULT + LOSE)
    client2.send(PLAY_RESULT + WIN)


def run_game(client1, client2):
    """Runs the game for the two clients until they close the connection"""
    start_game(client1, client2)
    while True:
        card1 = recv_command(client1)
        card2 = recv_command(client2)
        if card1 is None or card2 is None:
            break
        card1 = parse_card(card1)
        card2 = parse_card(card2)
        if (card1 < 0 or card1 > 51) or (card2 < 0 or card2 > 51):
            break
        compare_cards(card1, card2, client1, client2)


def recv_command(client):
    """Receives data from a client and parses
    it to return usable information"""
    data = client.recv(RESPONSE_LENGTH)
    if data == WANT_GAME:
        data = client.recv(RESPONSE_LENGTH)
        if data == WANT_GAME:
            return b'-1'
    elif data == PLAY_CARD:
        return client.recv(RESPONSE_LENGTH)
    return None


def run_server(server):
    """Runs the server from two clients to play a War Game"""
    conn1 = server.accept()[0]
    conn2 = server.accept()[0]
    want_game = 0
    while True:
        data1 = recv_command(conn1)
        data2 = recv_command(conn2)
        if data1 == b'-1':
            want_game = want_game + 1
        if data2 == b'-1':
            want_game = want_game + 1
        if want_game == 2:
            run_game(conn1, conn2)
            break
    conn1.close()
    conn2.close()


args = sys.argv
if len(args) == 2:
    server_socket = socket.socket()
    server_socket.bind(("127.0.0.1", int(args[1])))
    server_socket.listen(3)
    run_server(server_socket)
    server_socket.close()
else:
    print("Input should only have one additional argument")
