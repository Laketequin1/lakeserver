import socket, threading, ast # Imports for client and server

class Server:
    
    def __init__(self, port, header=64, format='utf-8'): #  Default: header is 64 bytes long, format is utf-8
        
        self.PORT = port # Port
        self.HEADER = header # Size of header before data sent
        self.FORMAT = format # Format of text being sent
        
        self.SERVER_IP = socket.gethostbyname(socket.gethostname()) # Computer IP (LAN)
        self.ADDR = (self.SERVER_IP, self.PORT) #Server address
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates server on "INET", and sock stream means we are streaming data
        self.server.bind(self.ADDR) # Binds address to server
        
        self.data = {'commands':[], 'data':[]} # Stores the commands and data of every connection, will be sent to all computers
    
    def start(self):
        self.server.listen() # Activates server, and will listen for pings
        
        print(f"Server is listening on {self.SERVER_IP}") # Prints the IP we are running on
        
        while True: # Continually adds new connections
            
            client_conn, client_addr = self.server.accept() # Waits for a new connection to join the server and gets IP
            
            thread = threading.Thread(target=self.handle_client, args=(client_conn, client_addr)) # Creates a new thread for this specific connection, with handle_client()
            thread.start() # Starts thread
            
            print(f"[INFO] Active threads: {threading.activeCount() - 1}") # prints how many connections we have on the server, from the amount of threads runnning
    
    def recieve_message(self, client_conn): # Recieves massage from a client
	
        client_message_length = client_conn.recv(self.HEADER).decode(self.FORMAT) # Waits for message lenght of next message and decodes from format
        
        if client_message_length: # Makes sure that there is a message
            client_message_length = int(client_message_length)
            client_message = self.conn.recv(client_message_length).decode(self.FORMAT) # Waits for message and decodes from format
            return client_message
    
    def send_message(self, message, conn): # Send message to a client
	
        encoded_message = message.encode(self.FORMAT) # Encodes message
        encoded_message_length = len(encoded_message) # Gets encoded message length
        header_message = str(encoded_message_length).encode(self.FORMAT) # Set header message to the string of the lenght and incode with format
        header_message += b' ' * (self.HEADER - len(header_message)) # Adds blanks to the end to make the header_message the right size
        conn.send(header_message) # Header sends the message length of main message
        conn.send(encoded_message) # Sends the message in encoded format
    
    def handle_client(self, client_conn, client_addr): # Given a thread for each connection, gets the clients IP
        
        clients_data = [] # Stores data recieved
        
        self.data['data'].append({client_addr:[]}) # Adds this client to the data list
        
        connected = True
        while connected:
            
            self.send_message(f"{self.data}", client_conn) # Sends message with server data
            
            client_message = self.recieve_message(client_conn) # Runs recieve message function, and gets message
            
            if client_message: # If message recieved has a value
                
                for command in client_message['commands']: # Go through every command
                    if command == "disconnect": # If command disconnect
                        connected = False # End thread
                    
                for client_data_section in client_message['data']: # For each piece of data
                    client_addr[client_data_section.key()] = client_data_section.value() # Store data in its spcific IP                
            
            print(f"Data: {client_message}") # Prints client message
            
        del self.data['data'].key(client_addr) # Remove persons data from server data
        client_conn.close() # Closes the connection between the client

class Client:
    def __init__(self, server_ip, port, header=64, format='utf-8'): #  Default: header is 64 bytes long, format is utf-8
        
        self.SERVER_IP = server_ip # The IP of the host (public IP for non-lan, private IPV4 for lan)
        self.PORT = port # Port
        self.HEADER = header # Size of header before data sent
        self.FORMAT = format # Format of text being sent
        
        self.SERVER_IP = socket.gethostbyname(socket.gethostname()) # Computer IP (LAN)
        self.ADDR = (self.SERVER_IP, self.PORT) #Server address
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates server on "INET", and sock stream means we are streaming data
        self.server.bind(self.ADDR) # Binds address to server
        
        self.data = {'commands':[], 'data':[]} # Stores the commands and data being sent to server    


main_server = Server(5050)