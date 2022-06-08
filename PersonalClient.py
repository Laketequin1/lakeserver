import socket #imports
import threading
import ast

HEADER = 64 #Set size for first text lengh
PORT = 5050 #Port number for server
SERVER = "10.13.1.107" #The ip that the host is running on (public IP for non lan, private IPV4 for lan)
ADDRESS = socket.gethostbyname(socket.gethostname()) #This computers IP (LAN)
ADDR = (SERVER, PORT) #Server address
FORMAT = "utf-8" #encoding format

x = 5 #setting test values
y = 6

data = [] #setting test data as list
data.append(x)
data.append(y)

serverData = [] #data recieved from server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connects client to INET, streaming data
client.connect(ADDR) #binds connected address to above


def recieve_message(): #recieves massage from server
	
	serverMessageLength = client.recv(HEADER).decode(FORMAT) #waits for a message, when it gets it, decodes from utf-8
	
	if serverMessageLength: #makes sure that there is a message
		
		serverMessageLength = int(serverMessageLength) #turns message lenght from a string to a number
		serverMessage = client.recv(serverMessageLength).decode(FORMAT) #gets the real message, and decodes it
		return serverMessage #returns the message back to the previous function


def send_message(messageToSend): #function to send message to server
	
	encodedMessageToSend = messageToSend.encode(FORMAT) #encodes message
	messageToSendLength = len(encodedMessageToSend) #gets message length
	messageLengthOfMessage = str(messageToSendLength).encode(FORMAT)
	messageLengthOfMessage += b' ' * (HEADER - len(messageLengthOfMessage)) #creates the first message to send, holding the number, adds bites of space to make exactyly HEADER long
	client.send(messageLengthOfMessage) #sends the message length
	client.send(encodedMessageToSend) #sends the message in encoded format


def handle_server():
	
	global data
	global serverData
	
	while True:
		serverMessage = recieve_message() #waits to recieve message, and applies it to serverMessage
		
		if serverMessage[0] == "@": #if message is Data (shown by @)
			serverData = serverMessage[1:len(serverMessage)] #gets the actual data
			serverData = ast.literal_eval(serverData) #converts data string into list
		
		data = [] #setting player co-ords
		data.append(x)
		data.append(y)
		
		send_message(f"@{data}") #sends message data
	
	
thread = threading.Thread(target=handle_server) #creates a new thread for this specific connection, with handle_client()
thread.start() #starts thread



import pygame #Imports
import time
import random
import sys
from pygame import mixer
pygame.init()
mixer.init()

def RUN(): #Run game
	global x
	global y
	global data
	global serverData
	
	dis_width = 1200 #Screen Width/Height
	dis_height = 800
	
	tickSpeed = 300 #game speed
	
	blue = (70, 100, 255) #Colour setting
	lightBlue = (70, 70, 255)
	red = (255, 100, 100)
	green = (100, 255, 100)
	
	x = 587 #Character X, Y
	y = 387
	
	running = True
	
	clock = pygame.time.Clock()#Game Speed
	
	dis = pygame.display.set_mode((dis_width, dis_height)) #Screen Creation
	pygame.display.set_caption("Hit or Miss")
	
	#Makes Game Run
	while running == True:
		
		for event in pygame.event.get():#Exit Button
			if event.type == pygame.QUIT:
				running = False
		
		dis.fill(blue) #Create images
		pygame.draw.rect(dis, lightBlue, [50, 50, 1100, 700])
		
		tickSpeed = 300
		
		pressed = pygame.key.get_pressed()#Controller
		if pressed[pygame.K_d]:
			x += 1.5
		if pressed[pygame.K_a]:
			x -= 1.5
		if pressed[pygame.K_w]:
			y -= 1.5
		if pressed[pygame.K_s]:
			y += 1.5
		
		if x > 1125: # Borders
			x = 1125
		elif x < 50:
			x = 50
		if y > 725:
			y = 725
		elif y < 50:
			y = 50
		
		data = []

		data.append(x)
		data.append(y)
		
		cloneServerData = serverData
		
		if cloneServerData:
			for number in range(len(cloneServerData)):#loop for each enemy
				try:
					pygame.draw.rect(dis, red, [cloneServerData[number-1][1][0], cloneServerData[number-1][1][1], 25, 25])
				except Exception:
					pass
		
		pygame.draw.rect(dis, green, [x, y, 25, 25])
		
		pygame.display.flip()#Load Screen
		clock.tick(tickSpeed)#Game Speed
	
	
RUN()
