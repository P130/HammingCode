""" Hamming code (7,4) """

import socket  # Import socket module
import numpy as np # Import numpy module

H = np.array([[1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1]])     # H array will be used to check for errors
R = np.array([[0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]]) # R array will be used to decode the message
word_array = np.array([0, 0, 0, 0, 0, 0, 0])    # word_array will hold the received message from client
L = 7       # every 7 bits of encoded message must be decoded to 4


def main():
    try:
        s = socket.socket()  # Create a socket object
        host = socket.gethostname()  # Get local machine name
        port = 9992  # Reserve a port for your service.
        s.bind((host, port))  # Bind to the port
        print("Server running...")
        s.listen(5)      # Now wait for client connection.
    except socket.error as msg:
        print("Socket creation error: " + str(msg))
    while True:
        c, addr = s.accept()    # Establish connection with client.
        print('Got connection from', addr)
        c.send(str.encode('Server:-Thank you for connecting!'))  # Send a message to client

        encoded_word = ''        # Declaration of encoded_word
        decoded_word = ''        # Declaration of decoded_word

        encoded_word = str(c.recv(1024), "utf-8")   # Receive the entire encoded message from client

        print("Binary format of encoded message: " + encoded_word)
        print("Decoding...")
        while len(encoded_word) >= L:               # For every 7 bits of encoded message
            bitstodecode = encoded_word[0:L]
            fill_array(bitstodecode)                # fill with them the word_array
            corrected_array = parity_check(word_array)
            decoded_word += hamming_decode(corrected_array)  # Retrieves the (fixed if errors occured) binary form of encoded message and decodes it

            encoded_word = encoded_word[L:]         # proceed to the next 7 bits




        print("Decoded binary format of what client sent: " + decoded_word)
        print("Client sent: " + ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(decoded_word)]*8)))

        c.close()  # Close the connection

def fill_array(word):  # Fills global word_array ,using the received message , to use it for later calculations

    for i in range(0, 7):
        word_array[i] = word[i]

def hamming_decode(word_arr): # Decodes the received message by multiplying the 7-bit array(word_arr) with R array

    decoded_array = R.dot(word_arr)
    decoded_string = ''
    for i in range(0, 4):
        decoded_string += str(decoded_array[i])
    return decoded_string


def parity_check(word_arr):           # Checks the received message for errors and fixes them if they exist
    parity_array = H.dot(word_arr)     # Multiplies the 7-bit array(word_arr) with H array and stores the result to parity array

    parity_array[0] %= 2                # Converts the elements of parity to 0 and 1
    parity_array[1] %= 2
    parity_array[2] %= 2

    if (parity_array[0] != 0) or (parity_array[1] != 0) or (parity_array[2] != 0):

        parity_string = ''

        parity_string = str(parity_array[2]) + str(parity_array[1]) + str(parity_array[0]) # Find the position of the error
        error_pos = int(parity_string, 2) - 1
        print("Error occured at the " + str(error_pos) + " bit of word: " + str(word_arr) + ". We took care of it :D")
        if word_arr[error_pos] == 0:  # If word_arr[err_position] = 0 make it 1
            word_arr[error_pos] = 1
        else:  # else make it 0
            word_arr[error_pos] = 0

    return word_arr



main()      # main will run first