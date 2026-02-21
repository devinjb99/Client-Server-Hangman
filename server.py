import random
import socket
import time
from hangman import hangman

s = socket.socket()

port = 100
localHost = '127.0.0.1'
s.bind((localHost, port))
print("Server listening on: Localhost on port: ", port)
s.listen(1)
conn, addr = s.accept()
hangmanWordDictionary = ["habitual", "offbeat", "increase", "scold", "treat", "blushing", "payment", "offer",
                         "bashful", "ten", "burst", "can", "leg", "full", "truthful", "sell",
                         "disgusted", "swift", "dispose", "saddle","abide", "shaggy", "war", "gullible", "error",
                         "leak", "apologize", "stink","knot", "brother", "sever", "infamous", "sashay", "silent", "horn",
                         "help", "change", "way", "comparison", "triumph", "wasabi", "danielle", "swirls"]
tries = 6
print(f"Connected by {addr}")
print("Waiting for message...")
clientMessage = conn.recv(4096).decode()
print(clientMessage)
print("type /q to quit OR 'game' to play hangman")
print("Send message")
while True:
    if clientMessage == "/q":
        break
    if clientMessage == "game":
        print("We are now playing hangman!")
        print("They have 6 tries to guess a letter in a word until they complete the word\n")
        attempt = 0
        hiddenWord = ''
        won = False
        wordToGuess = random.choice(hangmanWordDictionary)
        print("The word they needs to guess is:", wordToGuess)
        for i in range(len(wordToGuess)):
            hiddenWord += '_'
        while attempt <= tries:
            serverMessage = hangman(attempt)
            conn.sendall(serverMessage.encode())
            serverMessage = hiddenWord
            conn.sendall(serverMessage.encode())
            clientMessage = conn.recv(4096).decode()
            if len(clientMessage) > 1 or not clientMessage.isalpha():
                print("INVALID ENTRY")
                serverMessage = "INVALID ENTRY Try again"
                conn.sendall(serverMessage.encode())
            elif clientMessage not in wordToGuess:
                attempt += 1
                if attempt >= tries:
                    break
                serverMessage = "Letter not in word Try again"
                conn.sendall(serverMessage.encode())
            else:
                print("Letter {0} is in the word!".format(clientMessage))
                hiddenWord_as_list = list(hiddenWord)
                whereLetterIs = [i for i, ltr in enumerate(wordToGuess) if ltr == clientMessage]
                for i in whereLetterIs:
                    hiddenWord_as_list[i] = clientMessage
                hiddenWord = "".join(hiddenWord_as_list)
                if hiddenWord == wordToGuess:
                    won = True
                    serverMessage = "You found the word!"
                    conn.sendall(serverMessage.encode())
                    time.sleep(.5)
                    serverMessage = wordToGuess
                    conn.sendall(serverMessage.encode())
                    break
                else:
                    serverMessage = "keep going"
                    conn.sendall(serverMessage.encode())
        if won:
            print("They Won!")
        else:
            print("They Lost!")
            serverMessage = "You did not find the word!"
            conn.sendall(serverMessage.encode())
        time.sleep(2)
        print("Send a msg to client....")

    serverMessage = input()
    conn.sendall(serverMessage.encode())
    clientMessage = conn.recv(4096).decode()
    print(clientMessage)
print("Client has now left the chat.....")
s.close()
