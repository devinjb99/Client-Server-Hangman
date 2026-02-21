import socket
import time
localHost = socket.gethostbyname('127.0.0.1')
port = 100
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((localHost, port))
print("Connected to: localhost On port: ", port)
print("type /q to quit OR 'game' to play hangman")
print("Send message")
while True:
    clientMessage = input()
    s.sendall(clientMessage.encode())
    if clientMessage == "/q":
        break
    if clientMessage == "game":
        serverMessage = ''
        print("You have 6 tries to guess a letter in a word until you complete the word")
        while True:
            serverMessage = s.recv(4096).decode()
            print(serverMessage)
            serverMessage = s.recv(4096).decode()
            print(serverMessage)
            print("Guess a letter")
            clientMessage = input()
            s.sendall(clientMessage.encode())
            serverMessage = s.recv(4096).decode()
            if serverMessage == "You found the word!":
                print(serverMessage)
                serverMessage = s.recv(4096).decode()
                print(serverMessage)
                print("You win!")
                break
            if serverMessage == "You did not find the word!":
                print(serverMessage)
                print("You lose!")
                break
        print("GAME OVER")
        print("Wait for server to talk to you....")
    serverMessage = s.recv(4096).decode()
    print(serverMessage)

s.close()
