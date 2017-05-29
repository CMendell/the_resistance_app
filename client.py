# -*- coding: UTF-8 -*-

'''Connor Mendell
Class: CSI 235-01
​ Assignment: Lab 7
Date Assigned: April 10
Due Date: April 17
Description:
Connects to a server, sends a question and receives a magic 8 ball answer
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
import time

HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1024


def create_socket_and_connect():

    #Pre: a proper host and port number
    #Post: A connected socket
    #Purpose: create socket with access to items in framing.py

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( (HOST, PORT) )
    print 'Client connected and assigned socket name ', sock.getsockname()
    return framing.FramingSocket(sock)


def check_message():
    # Pre: None
    # Post: A properly formatted message for sending
    # Purpose: Ensure that the message to be sent is properly formatted
    while True:
        question_mark = False
        message = raw_input("Please enter a question without any question marks in it: ")
        length = len(message)
        for i in range(length):
            if message[i] == '?':
                question_mark = True
                continue
        if question_mark:
            print 'ERROR please type a question without a question mark in it... \n'
            continue
        else:
            return message


sock = create_socket_and_connect()
while True:
    message = check_message()
    sock.send_delimiter_terminated_message(message, '?')
    print sock.recv_until_delimiter('.', BUFFER_SIZE)
    choice = raw_input('Keep asking question (y/n): ')
    if choice == 'n':
        sock.send_delimiter_terminated_message('DISCONNECT', '?')
        time.sleep(1.0)
        sock.close()
        break
    elif choice == 'y':
        continue
