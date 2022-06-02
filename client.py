#importing required modules

from email import message
import socket
import threading



def communicate_to_server(client):
    # send username

    username = input("Enter your username: ")
    if username != '':
        client.sendall(username.encode())
    else:   
        print("Username is empty")
        exit(0)
    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    send_message_to_server(client,message)

def send_message_to_server(client,message):
    
    while 1:
        message = input("")
        if message != '':
            client.sendall(message.encode())
     
    
        else:
            print("The msg is empty ")
            exit(0)

def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf_8')
        if message !='':
            # username = message.split("~")[0]
            # content = message.split("~")[1]

            print(f"{message}")
        else:
            print("The msg is empty ")

HOST = '127.0.0.1'
PORT  = 1234
def main():
    client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

    try:
        client.connect((HOST, PORT))
        print("Connected")
    except:
        print("Connection failed")

    communicate_to_server(client)

def bid_for_player():
    pass
def show_purse_all():
    pass
def player_list():
    pass

if __name__=='__main__':
    main()