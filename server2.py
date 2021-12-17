#Akhilesh Mosale Nagabhushana
#1001848441


import socket
import time
import pickle
import os

#https://pythonprogramming.net/sockets-tutorial-python-3/
#Specifying Header size
HeaderSize = 70

#https://steelkiwi.com/blog/working-tcp-sockets/
#Creating the socket, AF_INET == ipv4, SOCK_STREAM == TCP
SocketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Specifying IP address and port number. (1245 is Port number for connection with Server A)
SocketConn.bind((socket.gethostname(), 1246))
#Waiting for Server A to send request
SocketConn.listen(5)

while True:
    Client_Socket, Address_Client = SocketConn.accept()
    print(f"Connection from {Address_Client} has been established.")
    # Creating dictionaries and lists to manipulate data
    c={}
    d = {}
    NameList = []
    SizeList = []
    LastModifiedList = []
    # Getting list of file names from current directory
    for name in os.listdir('.'):
        NameList.append(name)
        NameList.sort(key=lambda v: v.upper())

    for name in NameList:
        #https://flaviocopes.com/python-get-file-details
        # Getting the last modified date of each file and appending to a list
        LastModifiedList.append(time.ctime(os.path.getmtime(name)))
        # Converting size from bytes to kilobytes
        SizeInBytes = (os.path.getsize(name)) / 1024
        size=str(round(SizeInBytes,2)) +"KB"
        # Appending size of each file to a list
        SizeList.append(size)
    # Updating the created dictionary
    c.update({"Name": NameList,"Size":SizeList,"Time":LastModifiedList})
    #Assigning c to final dictionary
    d=c
    # Sending the data to the Server A (Includes data from B)
    Message = pickle.dumps(d)
    Message = bytes(f"{len(Message):<{HeaderSize}}", 'utf-8')+Message
    Client_Socket.send(Message)