# -*- coding: UTF-8 -*-

'''Connor Mendell
Class: CSI 235-01
​ Assignment: Lab 7
Date Assigned: April 10
Due Date: April 17
Description:
Basic framing stuff for a client and server
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

#Some code from CSI-235-01 inspired these functions

class FramingSocket(object):
    def __init__(self, sock):
        #Pre:  a socket object
        #Post: initializes values for the class
        #Purpose: properly setup class values for later use

        self.sock = sock
        self.__recv_buffer = b""

    def recv_until_delimiter(self, delimiter, buffer_size):
        # Pre: a delimiter character and a size in bytes for the buffer
        # Post: get the message sent from either server or client
        # Purpose: to ensure that the receiver gets the entirety of a message up to the delimiter character
        data = b''
        while True:
            if self.__recv_buffer:
                more = self.__recv_buffer
                self.__recv_buffer = b""
            else:
                more = self.sock.recv(buffer_size)
                if not more:
                    raise EOFError("Socket was closed before delimiter was"
                                   + " reached.  Received: {!r}".format(data))
            delimiter_index = more.find(delimiter)
            if delimiter_index > -1:
                data += more[:delimiter_index]
                self.__recv_buffer = more[delimiter_index + len(delimiter):]
                break
            data += more
        return data

    def send_delimiter_terminated_message(self, message, delimiter):
        # Pre: a message and the proper delimiter
        # Post: sends a message plus the designated delimiter
        # Purpose: To send a message that ends with a delimiter character
        self.sock.sendall(message + delimiter)

    def close(self):
        # Pre: a socket
        # Post: a closed socket
        # Purpose: to close a socket
        self.sock.close()