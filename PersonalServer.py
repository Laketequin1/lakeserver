import threading #imports
import socket
import ast

HEADER = 64 #Set size for first text lengh
PORT = 5050 #Port number for server
SERVER = socket.gethostbyname(socket.gethostname()) #Computer IP (LAN)
ADDR = (SERVER, PORT) #Server address
FORMAT = "utf-8" #encoding format

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates server on "INET", and sock stream means we are streaming data
server.bind(ADDR) #binding the server address to the server

data = [] #where we store all the games data, and who it belongs to

def start(): #starting loop
	
	server.listen() #activates server, and will accept pings
	print(f"Server is listening on {SERVER}") #tells us what IP we are running on, and that we have succesfully started the server
	
	while True: #true loop, adding new connections
		
		conn, addr = server.accept() #waits for a new connection to join the server
		
		thread = threading.Thread(target=handle_client, args=(conn, addr)) #creates a new thread for this specific connection, with handle_client()
		thread.start() #starts thread
		
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") #tells us how many connections we have on the server, from the amount of threads runnning.


def recieve_message(conn): #recieves massage from client
	
	clientMessageLength = conn.recv(HEADER).decode(FORMAT) #waits for a message, when it gets it, decodes from utf-8
	
	if clientMessageLength: #makes sure that there is a message
		
		clientMessageLength = int(clientMessageLength) #turns message lenght from a string to a number
		clientMessage = conn.recv(clientMessageLength).decode(FORMAT) #gets the real message, and decodes it
		return clientMessage #returns the message back to the previous function


def send_message(messageToSend, conn): #function to send message to client
	
	encodedMessageToSend = messageToSend.encode(FORMAT) #encodes message
	messageToSendLength = len(encodedMessageToSend) #gets message length
	messageLengthOfMessage = str(messageToSendLength).encode(FORMAT)
	messageLengthOfMessage += b' ' * (HEADER - len(messageLengthOfMessage)) #creates the first message to send, holding the number, adds bites of space to make exactyly HEADER long 
	conn.send(messageLengthOfMessage) #sends the message length
	conn.send(encodedMessageToSend) #sends the message in encoded format

def handle_client(conn, addr): #given a thread for each connection, gets the clients IP
	
	global data #makes the game data avalable to the every function and thread
	
	connected = True #makes while loop run
	
	while connected: #while not recieved !DISCONNECT
		
		send_message(f"@{data}", conn) #sends message hello
		
		clientMessage = recieve_message(conn) #runs recieve massage function, and gets message
		
		if clientMessage == "!DISCONNECT": #find if the clients message is the disconnect message
			connected = False #atop the loop
			
		elif clientMessage[0] == "@": #if message is returning data (shown by having @ at start of string)
			clientData = clientMessage[1:len(clientMessage)] #clients data saved to clientData
			clientData = ast.literal_eval(clientData) #turns data string of list into list
			
		foundItem = 0 #checks if we have set
		
		for item in data: #for client and its data in data
			if item[0] == addr: #if item address the same as this clients address
				data[data.index(item)][1] = clientData #if found address == this clients address, set its data to new data
				foundItem = 1 #found item
			
		if foundItem == 0: #if address not in data list
			dataSetter = [] #sets client address and its data to a list
			dataSetter.append(addr)
			dataSetter.append(clientData)
			data.append(dataSetter) #sets this clients list to the main list
		
		print(f"Data: {data}")#sends message
		
	conn.close() #closes the connection between the client, before finishing the function, ending the thread
		
		

start() #starts
