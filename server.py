# Akhilesh Mosale Nagabhushana
# 1001848441

import socket
import sys
import time
import pickle
import os
from dirsync import sync
from threading import Timer
import threading
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


HeaderSize = 70


SocketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SocketConn.bind((socket.gethostname(), 1243))

SocketConn.listen(5)

while True:

    # Creating new socket connection for Server B
    SecondConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #1245 is the new Port number for Server A to connect with Server B
    SecondConn.connect((socket.gethostname(), 1246))

    # Provide servera path and severb path here
    source_path = "/home/akhilesh/DS project/servera"
    target_path = "/home/akhilesh/DS project/serverb"

    # https://www.titanwolf.org/Network/q/db9c4cf2-3054-4e98-8267-70af2f749bdc/y
    sync(source_path, target_path, 'sync')
    sync(target_path, source_path, 'sync')


    # https://realpython.com/python-logging/
    def log():
        logging.basicConfig(format='', level=logging.INFO)
        logging.info('')

    # Syncing the directories based on number of files
    def f(f_stop):
        # https://stackoverflow.com/questions/54688687/how-to-synchronize-two-folders-using-python-script
        if len(os.listdir(source_path)) > len(
                os.listdir(target_path)):
            sync(target_path, source_path, 'sync', purge=True, logger=log())
        elif len(os.listdir(source_path)) < len(
                os.listdir(target_path)):
            sync(source_path, target_path, 'sync', purge=True, logger=log())
        else:
            sync(source_path, target_path, 'sync', twoway=True, logger=log())
            sync(target_path, source_path, 'sync', twoway=True, logger=log())

        # https://newbedev.com/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
        if not f_stop.is_set():
            threading.Timer(5, f, [f_stop]).start()
    # Watchdog function to monitor directory a
    # https://michaelcho.me/article/using-pythons-watchdog-to-monitor-changes-to-a-directory
    def watchfunc1():
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        path = source_path
        event_handler = LoggingEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()


    # Watchdog function to monitor directory b
    def watchfunc2():
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        path = target_path
        event_handler = LoggingEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()

    # https://newbedev.com/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
    f_stop = threading.Event()
    f(f_stop)

    # https://stackoverflow.com/questions/50593200/flask-application-with-watchdog-observer
    # Assigning watchdog function a thread
    th = threading.Thread(target=watchfunc1)
    # Start the thread
    th.start()
    # Wait for thread to finish
    th.join()
    # https://stackoverflow.com/questions/2905965/creating-threads-in-python
    # Assigning watchdog function another thread
    th = threading.Thread(target=watchfunc2)
    # Start the thread
    th.start()
    # Wait for thread to finish
    th.join()

    #Server A acts like a client and sends request to Server B
    while True:
        # Sender is sending data in bytes and not characters hence we add 'b'
        Sender_Msg = b''
        # Boolean to check if the message is new
        IsNewMsg = True
        while True:
            # https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
            # Receiving the data from server
            Message = SecondConn.recv(1000)
            # Checking if message is new
            if IsNewMsg:
                msglen = int(Message[:HeaderSize])
                IsNewMsg = False

            Sender_Msg += Message

            # If len(Sender_Msg)-HeaderSize == MessageLength is true then we have received full message
            if len(Sender_Msg) - HeaderSize == msglen:
                #https://docs.python.org/2/library/pickle.html
                #Using pickle to load the data
                d = (pickle.loads(Sender_Msg[HeaderSize:]))
                IsNewMsg = True
                Sender_Msg = b""
                keys = list(d.keys())
                #Receiving data from Server B and appending to a list
                x = []
                for key, value in d.items():
                    x.append(value)
            #Adhering to Client's request (Server A)
            Client_Socket, Address_Client = SocketConn.accept()
            print(f"New Connection from {Address_Client} is established.")


            #Creating dictionaries and lists to manipulate data


            c={}
            d = {}
            NameList = []
            SizeList = []
            LastModifiedList = []
            NewNameList=[]
            NewSizeList=[]
            NewLastModifiedList = []
            #Getting list of file names from current directory
            for name in os.listdir('.'):
                NameList.append(name)
                NameList.sort(key=lambda v: v.upper())
            #Appending the list of directories from server A with directories of Server B
            #NewNameList=NameList+x[0]
            NewNameList = NameList
            #Sorting the list based on Name
            NewNameList.sort(key=lambda v: v.upper())


            for name in NameList:
                #https://flaviocopes.com/python-get-file-details
                #Getting the last modified date of each file and appending to a list
                LastModifiedList.append(time.ctime(os.path.getmtime(name)))
                #Converting size from bytes to kilobytes
                SizeInBytes = (os.path.getsize(name)) / 1024
                size=str(round(SizeInBytes,2)) +"KB"
                #Appending size of each file to a list
                SizeList.append(size)
            #Appending sizelist with list of files from directory of Server B
            #NewSizeList=SizeList+x[1]
            NewSizeList = SizeList
            # Appending last modified list with list of files from directory of Server B
            #NewLastModifiedList=LastModifiedList+x[2]
            NewLastModifiedList = LastModifiedList
            #Updating the created dictionary
            c.update({"Name": NewNameList,"Size":NewSizeList,"Time":NewLastModifiedList})
            #Adding to another dictionary for display purpose
            d=c
            #Sending the data to the client (Includes data from server A and server B)
            Message = pickle.dumps(d)
            Message = bytes(f"{len(Message):<{HeaderSize}}", 'utf-8')+Message
            Client_Socket.send(Message)
