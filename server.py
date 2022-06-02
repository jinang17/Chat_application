# importing required modules
from email import message
from encodings import utf_8
from pickle import TRUE
from re import X
import socket
import threading
from time import sleep
from turtle import Turtle
from urllib import response
import random
import pandas as pd
import numpy as np


HOST = '127.0.0.1'
#We have used localhost here so we have used 127.0.0.1
PORT = 1234
#We have used the port to make server and client communicate
Auction_completed = False
# Main fucntion
LISTENER_LIMIT = 2 
# This is the limit of the number of clients that can connect to the server
active_clients = []  
# List of all active clients


def new_func():
    # New function for checking that all client have came or not 
    while Auction_completed == False:
        Auction_start_bool = False
        print(len(active_clients))
        if len(active_clients) == 2:
            Auction_start_bool = True
        sleep(10)
        while Auction_start_bool:
            #IF all teams have entered the auction 
            start_Auction()


def start_Auction():
    print("We are starting the auction")
    #
    Select_player()

    pass


def send_message_to_client(client, message):
    client.sendall(message.encode())


def send_message_to_all(message):

    for user in active_clients:
        send_message_to_client(user[1], message)


def listen_for_messages(client, username):
    while 1:

        message = client.recv(2048).decode('utf_8')
        if message != '':
            final_msg = username + ': ' + message
        if(current_bid_dicti[username] == -1):
            current_bid_dicti[username].append(message)

        else:
            print("The msg is empty ")


def client_handler(client):  # client here is the object of the socket
    # Server
    while 1:
        username = client.recv(2048).decode('utf_8')
        current_bid_dicti = {username: -1}
        print(current_bid_dicti)
        if username != '':
            active_clients.append((username, client))

            print(username, '~connected')
            client.send(bytes('Welcome to the chatroom', 'utf_8'))
            break

        else:
            print("Client username is empty ")

    threading.Thread(target=listen_for_messages,
                     args=(client, username)).start()


def main():
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Creating the socket class object
    # AF_INET is family of IPV4 addresses
    # SOCK_STREAM is TCP protocol
    # Binding the socket to the host and port

    try:
        server.bind((HOST, PORT))
        print("server is running ")
    except socket.error as e:
        print(str(e))

    # Setting server limit
    server.listen(LISTENER_LIMIT)
    threading.Thread(target=new_func, args=()).start()
    while 1:

        # Accepting the connection
        # This will return client and IPand port client is using
        client, address = server.accept()

        print('Connected to :', address[0], ':', address[1])
        threading.Thread(target=client_handler, args=(client,)).start()


bid_done = False
df = pd.DataFrame(pd.read_excel("PSC.xlsx"))
dictio = df.to_dict()
final_dict = {}
for i in range(0, 1000):
    final_dict[i] = [dictio['PLAYER'][i], dictio['TOTAL MATCHES PLAYED'][i], dictio['WIN %'][i], dictio['TOURNAMENTS WON']
                     [i], dictio['RUNS'][i], dictio['STRIKE RATE'][i], dictio['WICKETS'][i], dictio['ECONOMY RATE'][i], dictio['POINTS'][i]]

current_bid_dicti = {}
copy_dict = final_dict
Player_bool = []
sold_players_list = []
unsold_players_list = []
Teams = [[], []]
Purse = [80, 80]
Player_bool = np.zeros(1000, dtype=int)
Current_bid = np.ones(2, dtype='int')
Current_bid = Current_bid*-1


def start_Auction():
    print("We are starting the auction")
    Select_player()
    pass


def Select_player():
    all_visited = False
    print("Selecting the player")
    for i in Player_bool:
        if(i == 0):
            all_visited = True
    if(all_visited):
        final_func()

    current_player = random.choice(list(copy_dict))
    Player_bool[current_player] = '1'
    send_message_to_all(
        f"The current player for Bidding is {final_dict[current_player][0]}")
    send_message_to_all(
        f"Total matches Played by {final_dict[current_player][1]}")
    send_message_to_all(
        f"The win percentage in which the {final_dict[current_player][0]} played is {final_dict[current_player][2]}")
    send_message_to_all(
        f"Tournaments won by the {final_dict[current_player][0]} is {final_dict[current_player][3]}")
    send_message_to_all(
        f"The runs made by the {final_dict[current_player][0]} is {final_dict[current_player][4]}")
    send_message_to_all(
        f"The strike rate of {final_dict[current_player][0]} is {final_dict[current_player][5]} ")
    send_message_to_all(
        f"The Total wickets taken by {final_dict[current_player][0]} are {final_dict[current_player][6]}")
    send_message_to_all(
        f"The economy rate of {final_dict[current_player][0]} is {final_dict[current_player][7]}")
    send_message_to_all(
        f"The Total fantasy points of {final_dict[current_player][0]} are {final_dict[current_player][8]}")

    listen_to_bids(current_player)


def sold_player(Current_Player):

    # copy current_bid_dciti to current_bid list
    current_bid_list = []
    unsold_flag = True
    maxi = 0
    for i in current_bid_dicti:
        current_bid_list.append(current_bid_dicti[i])

    
    for i in Current_bid:
        if(i > 0):
            unsold_flag = False
    if(unsold_flag):
        unsold_players_list.append(Current_Player)
        Player_bool[Current_Player] = TRUE
        copy_dict.pop(Current_Player)
        Select_player()

    else:
        for i in Current_bid:
            if(i > maxi):
                i = maxi
        bid_winner = Current_bid(maxi)
        Teams[bid_winner].append([Current_Player, Current_bid])
        Purse[bid_winner] = Purse[bid_winner]-Current_bid
        sold_players_list.append(Current_Player)
        Player_bool[Current_Player] = TRUE
        copy_dict.pop(Current_Player)

        Select_player()


def listen_to_bids(current_player):

    while bid_done == False:
        for i in current_bid_dicti:
            if (current_bid_dicti == -1):
                bid_done = False
    if bid_done == True:
        sold_player(current_player)


def final_func():
    # Ahiya file handling and exit message close connections
    
    exit()
    # close the connections
    for client in active_clients:
        client.close()
    # close the server\

    pass


if __name__ == '__main__':
    main()
