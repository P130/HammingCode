""" Hamming code (7,4) """

import socket  # Import socket module
import math
import random

K = 4   # Every 4 bits of the message will be encoded
L = 7   # Every 7 bits of the encoded message will be sent to server

error = True


def connectwithServer():
    encodedbitword = ''  # this word will hold the entire message in bits
    s = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 9992  # Reserve a port for my service.
    s.connect((host, port))
    print(str(s.recv(1024), "utf-8"))  # Receives message from server
    msg = input('Write your message: ')  # This message will be sent to server
    rate = int(input('Submit the number of bits per which there will be one corrupted bit:(etc 100) '))
    bitword = ''.join('{0:08b}'.format(ord(x), 'b') for x in msg)  # message is converted to bits and it is stored in variable bitword

    print("Binary format of message: " + bitword)  # bitword is printed

    while len(bitword) >= K:  # every 4 bits
        nibble = bitword[0:K]  # the first 4 bits
        encodedbitword += hamming_encode(nibble)   # are being encoded with hamming code (7,4) eand the whole encoded message will be stored in encodedbitword
        bitword = bitword[K:]  # proceed to the next 4 bits

    print("Encoded binary format of message before adding noise: " + encodedbitword)  # print the encoded message

    """Here we add noise to the encodedbitword"""

    if rate != 0:
        li = list(encodedbitword)  # couldn't change the string so we converted the string to list and worked on that list
        temp = 0   # temp is the lower boundary of randint
        y = rate   # y is the upper boundary of randint
        length = len(encodedbitword)
        x = math.ceil(length / rate)  # the number of errors that will occur
        for i in range(0, x):
            if y >= length:
                y = length
            randomnum = random.randint(temp, y) - 1  # temp <= randnum <= y
            if li[randomnum] == '0':
                li[randomnum] = '1'
            else:
                li[randomnum] = '0'
            temp = y
            y += rate

        encodedbitword = ''.join(li)


    print("Encoded binary format of message after adding noise: " + encodedbitword)  # print the encoded message
    print("Sending data to server...")



    s.send(str.encode(encodedbitword))  # are being sent to server


    print("Process finished...")
    s.close  # Close the socket when done


def hamming_encode(bits):           # Return given 4 bits plus parity bits for bits (1,2,3), (1,3,4) and (2,3,4)
    p1 = parity(bits, [0, 1, 3])   # parity bit 1 corresponds to bits 1,2,4
    p2 = parity(bits, [0, 2, 3])   # parity bit 2 corresponds to bits 1,3,4
    p3 = parity(bits, [1, 2, 3])   # parity bit 3 corresponds to bits 2,3,4
    encoded = p1 + p2 + str(bits[0]) + p3 + str(bits[1]) + str(bits[2]) + str(bits[3])  # The format of encoded message will be p1 p2 b1 p3 b2 b3 b4
    return encoded


def parity(s, indexes):
    sub = ""
    for index in indexes:
        sub += s[index]
    return str(str.count(sub, "1") % 2)     # It counts the number of '1' and if the number is even then it returns 0 else if it is odd it returns 1





connectwithServer()  # connectwithServer will be the first function which will run
