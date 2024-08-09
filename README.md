# Lakeserver

A low-level networking protocol module for creating online games and chat servers. It supports peer-to-server connections with both server and client implementations. Utilizing multithreading, the server can handle multiple clients simultaneously. It features error handling and info outputs, which can be suppressed if info suppression is enabled. This project aims to help beginner programmers easily implement servers and multiplayer games without needing to understand TCP protocols or low-level networking systems.

Creating a server is as easy as three lines of code. 💪💪

## Server Example
```
from lakeserver import *

server = Server(5050) # Create new server on port 5050
server.start() # Start server
```

## Client Example
```
from lakeserver import *

client = Client("192.168.1.40", 5050) # Create a new client. Change the IP to the server's IP, and use the same port.
client.connect() # Connect client to server
```

## Expected Output
**Here is the expected output for the ServerTest.py file, which runs tests and shows users how to use the module.**
```

  #####                                        #######
 #     # ###### #####  #    # ###### #####        #    ######  ####  #####
 #       #      #    # #    # #      #    #       #    #      #        #
  #####  #####  #    # #    # #####  #    #       #    #####   ####    #
       # #      #####  #    # #      #####        #    #           #   #
 #     # #      #   #   #  #  #      #   #        #    #      #    #   #
  #####  ###### #    #   ##   ###### #    #       #    ######  ####    #

This is some example code for a server I created using socket. Made by Tequin Lake.


---Starting Server---
[Server INFO] Server IP: 192.168.1.40
[Server INFO] Server PORT: 5050
[Server INFO] Status: Ready
[Server INFO] New Connections: Allow

---Create Clients---
[Client INFO] Status: Ready
[Client INFO] Status: Ready
[Client INFO] Status: Ready

---Connect Client1---
[Client INFO] Status: Connected
[Server INFO] Client Event: Connected

---Sending/receiving client data---
Server data: {('192.168.1.40', 50570): ''}
Server data: {('192.168.1.40', 50570): '1'}
Server data: {('192.168.1.40', 50570): '1'}
Server data: {('192.168.1.40', 50570): '2'}
Server data: {('192.168.1.40', 50570): '6'}
Server data: {('192.168.1.40', 50570): '24'}
Server data: {('192.168.1.40', 50570): '120'}
Server data: {('192.168.1.40', 50570): '720'}
Server data: {('192.168.1.40', 50570): '5040'}
Server data: {('192.168.1.40', 50570): '40320'}
Server data: {('192.168.1.40', 50570): '362880'}
Server data: {('192.168.1.40', 50570): '3628800'}

---Disconnecting clients and shutting down server---
[Server INFO] Status: Starting Shutdown
[Client INFO] Status: Disconnecting
[Server INFO] Client Event: Disconnected
[Client INFO] Status: Disconnected
[Server INFO] Status: Shutdown
[Server INFO] New Connections: Deny

---Restarting server---
[Server INFO] Server IP: 192.168.1.40
[Server INFO] Server PORT: 5050
[Server INFO] Status: Ready
[Server INFO] New Connections: Allow

---Connecting 3 clients---
[Client INFO] Status: Connected
[Server INFO] Client Event: Connected
[Client INFO] Status: Connected
[Server INFO] Client Event: Connected
[Client INFO] Status: Connected
[Server INFO] Client Event: Connected

---Display server data---
Server data: {('192.168.1.40', 50573): '', ('192.168.1.40', 50574): '', ('192.168.1.40', 50575): ''}

---Client1 disconnects---
[Client INFO] Status: Disconnecting
[Client INFO] Status: Disconnected
[Server INFO] Client Event: Disconnected

---Display updated server data---
Server data: {('192.168.1.40', 50574): '', ('192.168.1.40', 50575): ''}

---Example error: Attempted to start running server---
[Server WARNING] Error: Server is currently active, shutdown the server before starting

---Disable [INFO] and [WARNING] messages---
Example error output for starting server:

---Enable [INFO] and [WARNING] messages---

---Disconnecting all clients and shutting down server---
[Server INFO] Status: Starting Shutdown
[Client INFO] Status: Disconnecting
[Client INFO] Status: Disconnecting
[Server INFO] Client Event: Disconnected
[Client INFO] Status: Disconnected
[Server INFO] Client Event: Disconnected
[Client INFO] Status: Disconnected
[Server INFO] Status: Shutdown
[Server INFO] New Connections: Deny

Press Enter to close...
```

## *License*

*Lakeserver is open-source and free to use. You are welcome to copy, modify, and distribute it as you see fit.*

*Made by Tequin Lake.*
