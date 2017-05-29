# -*- coding: UTF-8 -*-

'''Connor Mendell
Class: CSI 235-01
​ Assignment: Lab 7
Date Assigned: April 10
Due Date: April 17
Description:
returns a magic 8 ball answer to a client
Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition and
consequences of plagiarism and acknowledge that the assessor of this assignment
may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for the
- purpose of future plagiarism checking)
'''


import socket
import framing
from threading import Thread
from random import randint

SERVER_INTERFACE = ''
SERVER_PORT = 8080
BUFFER_SIZE = 4096


def accept(listener):
    # Pre: A listener object
    # Post: a connected socket
    # Purpose: to accept a connection

    print ('Waiting for a new connection')
    conn, address = listener.accept()
    print ('Accepted connection from ', address)
    print ('Socket name', conn.getsockname())
    print ('Socket peer', conn.getpeername())
    return conn, address


def accept_connections_forever(listener, total_player_num, player_num):
    # pre: a listener object
    # post: accepts connections forever and then handles the conversation
    # purpose: Allow the program to continually accept connections
    while True:
        conn, address = accept(listener)
        handle_conversation(conn, address, total_player_num, player_num)


def handle_conversation(sock, address, total_player_num, player_num):
    # Pre: a connected socket and the address of the client
    # Post: receives and sends proper messages
    # Purpose: the ensure that messages and replies are sent correctly and to catch any errors
    framed_socket = framing.FramingSocket(sock)
    print player_num
    while True:
        try:
            question = framed_socket.recv_until_delimiter('?', BUFFER_SIZE)
            if question == 'DISCONNECT':
                break
            else:
                number = randint(0, 19)
                #message = responses[number]
                #print question + '?'
                #framed_socket.send_delimiter_terminated_message(message, '.')
        except Exception as e:
            print ('Client {} error: {}'.format(address, e))
            sock.close()
            break
    sock.close()


def start_threads(listener, num_workers):
    # Pre:listener object and an int for number of strings
    # Post: creates threads for multiple clients
    # Purpose: to create a specified number of threads so multiple clients can connect
    player_num = 0
    for i in range(num_workers):
        args = (listener, num_workers, player_num)
        player_num += 1
        Thread(target=accept_connections_forever, args=args).start()

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind( (SERVER_INTERFACE, SERVER_PORT) )

    sock.listen(2)

    print ('Listening on port ' + str(SERVER_PORT))
    threads = raw_input('Please enter the number of players: ')
    NUM_PLAYERS = threads
    print NUM_PLAYERS
    print threads
    print('IMPORTANT!!!!!Please ask all players to connect nearly simultaneously')
    start_threads(sock, int(threads))
