#Akhilesh Mosale Nagabhushana
#1001848441

import socket
#https://docs.python.org/2/library/pickle.html
#Importing pickle for serializing and de-serializing a Python object
import pickle
import os
import stat
#https://pythonprogramming.net/sockets-tutorial-python-3/
#Specifying Header size
import sys

HeaderSize = 70

##https://pythonprogramming.net/sockets-tutorial-python-3/
#Creating the socket, AF_INET == ipv4, SOCK_STREAM == TCP
SocketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Specifying IP address and port number. (1243 is Port number for connection with Server A)
SocketConn.connect((socket.gethostname(), 1243))
b=True

if len(sys.argv)==1:
    #https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/
    while b:
        #Sender is sending data in bytes and not characters hence we add 'b'
        Sender_Msg = b''
        #Boolean to check if the message is new
        IsNewMsg = True
        while True:
            #https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
            #Receiving the data from server
            Received_Msg = SocketConn.recv(1000)
            #Checking if message is new
            if IsNewMsg:
                #Getting the length of the message
                MessageLength = int(Received_Msg[:HeaderSize])
                #Once data is received it is not a new Message
                IsNewMsg = False
            #Append the received message to Sender_Msg
            Sender_Msg += Received_Msg
            #https://www.youtube.com/watch?v=8A4dqoGL62E&list=RDCMUCfzlCWGWYyIQ0aLC5w48gBQ&index=5
            #If len(Sender_Msg)-HeaderSize == MessageLength is true then we have received full message
            if len(Sender_Msg)-HeaderSize == MessageLength:
                #https://stackoverflow.com/questions/15190362/sending-a-dictionary-using-sockets-in-python
                #Using pickle to load the data
                d=(pickle.loads(Sender_Msg[HeaderSize:]))
                #Setting back the boolean for next connection
                IsNewMsg = True
                #Getting the values from the dictionary
                keys = list(d.keys())
                x = []
                for key, value in d.items():
                    #Appending values to an empty list
                    x.append(value)
                #Formatting the list
                res = "\n".join("{}          {}          {}".format(x, y, z) for x, y, z in zip(x[0], x[1], x[2]))
                #Displaying the result
                print(res)
                exit()
else:
    NameList=[]
    for name in os.listdir('.'):
        NameList.append(name)
        NameList.sort(key=lambda v: v.upper())
    
    if sys.argv[1]=="-lock":
        LockedFile=NameList[int(sys.argv[2])]
        print(LockedFile)
        # https: // stackoverflow.com / questions / 16249440 / changing - file - permission - in -python
        #https://en.wikipedia.org/wiki/File-system_permissions
        os.chmod(LockedFile, 0o444)
        #os.chmod(LockedFile, 0x00000010)
    elif sys.argv[1]=="-unlock":
        LockedFile=NameList[int(sys.argv[2])]
        print(LockedFile)
        #https://en.wikipedia.org/wiki/File-system_permissions
        os.chmod(LockedFile, 0o777)


