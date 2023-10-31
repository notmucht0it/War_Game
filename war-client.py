"""
Kevin Monahan
CompSci 520 - Homework 3
10/30/2023
War Client
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
DECK_LENGTH = 26


def recv_command(client):
    """Receives data from the server and parses
    it to return usable information"""
    data = client.recv(RESPONSE_LENGTH)
    if data == GAME_START:
        return client.recv(DECK_LENGTH)
    if data == PLAY_RESULT:
        return client.recv(RESPONSE_LENGTH)
    return None


def win_or_lose(response):
    """Returns one if client won and zero otherwise"""
    if response == WIN:
        return 1
    return 0


def play_game(client):
    """Initiates call for a game of war. Runs for the length
    of the deck given to the client"""
    client.send(WANT_GAME + WANT_GAME)
    deck = recv_command(client)
    deck = list(deck)
    wins = 0
    while len(deck) > 0:
        card_num = random.randint(0, len(deck) - 1)
        client.send(PLAY_CARD+deck[card_num].to_bytes(1, "little"))
        # client.send(PLAY_CARD+b'\x34') #Bad send
        deck.pop(card_num)
        wins = wins + win_or_lose(recv_command(client))
    print(f"Client {client.getsockname()[1]} won {wins} games")


args = sys.argv
if len(args) == 3:
    client_socket = socket.socket()
    client_socket.connect((args[1], int(args[2])))
    play_game(client_socket)
    client_socket.close()  # close the connection
else:
    print("Input should only have two additional arguments")
