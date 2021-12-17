# DirectoriesSynchronization

This python project involves socket programming.
The overall outcome of this project includes synchronization of two directories, client requesting list of files from the server, locking certain files to prevent synchronization and unlocking those files to continue synchronization.

First install the following packages:
dirsync (pip install dirsync)
watchdog (pip install watchdog)

Create 2 directories as ServerA and ServerB
Place the files client.py and server.py in ServerA and place the file server2.py in ServerB
Create/Upload any files to the directories (for synchronization)

How to run the program:
Run the server2.py file py typing python3 server2.py (or py server2.py) in ServerB's terminal
In ServerA directory run the server.py file, after this we can see that the directories are synchronized.

![alt text](https://github.com/akhileshmosale/DirectoriesSynchronization/blob/main/img/1.png)

The client can request the list of files present at the server directory. The client can do so by running python3 client.py in ServerA's terminal

![alt text](https://github.com/akhileshmosale/DirectoriesSynchronization/blob/main/img/2.png)

The client can lock certain files so that they are prevented from synchronization. The client can do so by running python3 client.py -lock 2 ( where 2 in an index to denote the file in the directory, the index ranges from 0 to n)

![alt text](https://github.com/akhileshmosale/DirectoriesSynchronization/blob/main/img/3.png)

In ubuntu the file is displayed as locked:

![alt text](https://github.com/akhileshmosale/DirectoriesSynchronization/blob/main/img/4.png)

To continue synchronization the client can unlock the file using python3 client.py -unlock 2

![alt text](https://github.com/akhileshmosale/DirectoriesSynchronization/blob/main/img/5.png)


