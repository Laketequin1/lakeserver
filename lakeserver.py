import socket, threading, ast # Imports for client and server

class Server:
    
    ##### -- Init -- #####
    
    def __init__(self, port, header=64, format='utf-8'): #  Default: header is 64 bytes long, format is utf-8
        self.PORT = port # Port
        self.HEADER = header # Size of header before data sent
        self.FORMAT = format # Format of text being sent
        
        self.SERVER_IP = socket.gethostbyname(socket.gethostname()) # Computer IP (LAN)
        self.ADDR = (self.SERVER_IP, self.PORT) #Server address
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates server on "INET", and sock stream means we are streaming data
        self.server.bind(self.ADDR) # Binds address to server
        
        self.data = {'commands':[], 'data':""} # Stores the commands and data that will be sent to all computers
        self.client_data = {} # Stores the data recieved from every connection
        self.active_clients = 0 # Number of active client connections

        self.enable_outputs(True) # Outputs active
        
        self.info(f"Server IP: {self.SERVER_IP}") # Prints the IP the server is running on
        self.info(f"Server PORT: {self.PORT}") # Prints the PORT the server is running on
        self.info(f"Server status: Ready") # Prints that server is ready to start
    
    ##### -- Server Handling -- #####
    
    def start(self):
        thread = threading.Thread(target=self.connection_handler) # Creates a new thread for this specific connection, with handle_client()
        thread.start() # Starts thread
    
    def connection_handler(self):
        self.server.listen() # Activates server, and will listen for pings
        
        self.info(f"Server status: Active") # Prints that server is active
        
        while True: # Continually adds new connections
            client_conn, client_addr = self.server.accept() # Waits for a new connection to join the server and gets IP
            
            thread = threading.Thread(target=self.handle_client, args=(client_conn, client_addr)) # Creates a new thread for this specific connection, with handle_client()
            thread.start() # Starts thread
            
            self.active_clients += 1 # One more active connection
            
            self.info(f"Active threads: {self.active_clients}") # Prints how many connections we have on the server, from the amount of threads runnning
    
    ##### -- Client Handling -- #####
    
    def recieve_message(self, client_conn): # Recieves massage from a client
        client_message_length = client_conn.recv(self.HEADER).decode(self.FORMAT) # Waits for message lenght of next message and decodes from format
        
        if client_message_length: # Makes sure that there is a message
            client_message_length = int(client_message_length)
            client_message = client_conn.recv(client_message_length).decode(self.FORMAT) # Waits for message and decodes from format
            client_message = self.eval_message(client_message) # Converts data string into dict
            return client_message
    
    def send_message(self, message, client_conn): # Send message to a client
        encoded_message = message.encode(self.FORMAT) # Encodes message
        encoded_message_length = len(encoded_message) # Gets encoded message length
        header_message = str(encoded_message_length).encode(self.FORMAT) # Set header message to the string of the lenght and incode with format
        header_message += b' ' * (self.HEADER - len(header_message)) # Adds blanks to the end to make the header_message the right size
        client_conn.send(header_message) # Header sends the message length of main message
        client_conn.send(encoded_message) # Sends the message in encoded format
    
    def eval_message(self, message): # Changes string recieved to a dict
        try:
            return ast.literal_eval(message) # Converts data string into dict
        except Exception:
            self.warn(f"Error: Unable to eval message recieved") # If error
            return "" # Return empty
    
    def handle_client(self, client_conn, client_addr): # Given a thread for each connection, gets the clients IP
        self.client_data[client_addr] = "" # Adds this client to the client_data list with no data
        
        connected = True
        while connected:
            self.send_message(f"{self.data}", client_conn) # Sends message with server data
            
            client_message = self.recieve_message(client_conn) # Runs recieve message function, and gets message
            
            if client_message: # If message recieved has a value
                for command in client_message['commands']: # Go through every command
                    if command == "disconnect": # If command disconnect
                        connected = False # End thread
                        
                self.client_data[client_addr] = client_message['data'] # Store data in its spcific IP                
            
            self.info(f"Message: {client_message}") # Prints client message
            
        del self.client_data[client_addr] # Remove persons data from server data
        self.active_clients -= 1 # Remove one number from active connections
        client_conn.close() # Closes the connection between the client

    ### -- Print -- ###
    
    def warn(self, message): # Displays a warning message (ususally errors)
        if self.show_warnings == True: # If warning messages active
            print(f"[SERVER WARNING] {message}") # Print warning message
                
    def info(self, message): # Displays an informational message
        if self.show_info == True: # If info messages active
            print(f"[SERVER INFO] {message}") # Print warning message
    
    ##### -- Set -- #####
    
    def set_data(self, data): # Set the data being sent
        self.data['data'] = str(data)
        
    def add_command(self, command): # Add a command being sent to clients
        self.data['commands'].append(str(command))
    
    def remove_all_commands(self): # Remove all commands that will be sent to computers
        self.data['commands'] = []
    
    def enable_outputs(self, boolean): # Set outputs for warnings and info to active or inactive
        if type(boolean) == bool: # If input bool
            self.show_warnings = boolean # Warnings active/inactive
            self.show_info = boolean # Info active/inactive
        else:
            self.warn(f"Error: Bool {boolean} not valid for setting enable_outputs") # Error as type of input is not bool
        
    def enable_warnings(self, boolean): # Set outputs for warnings to active or inactive
        if type(boolean) == bool: # If input bool
            self.show_warnings = boolean # Warnings active/inactive
        else:
            self.warn(f"Error: Bool {boolean} not valid for setting enable_warnings") # Error as type of input is not bool
        
    def enable_info(self, boolean): # Set outputs for warnings to active or inactive
        if type(boolean) == bool: # If input bool
            self.show_info = boolean # Info active/inactive
        else:
            self.warn(f"Error: Bool {boolean} not valid for setting enable_info") # Error as type of input is not bool
    
    ##### -- Get -- #####
    
    def get_data(self): # Return server data
        return self.data['data']
    
    def get_commands(self): # Return server commands
        return self.data['commands']
    
    def get_client_data(self): # Return client data dict
        return self.client_data
    
    def get_server_ip(self): # Return server IP
        return self.SERVER_IP
    
    def get_server_port(self): # Return server PORT
        return self.PORT
    
    def get_number_of_active_clients(self): # Return number of clients connected to the server
        return self.active_clients
    
    def get_all_outputs_enabled(self): # Return True if warnings and info are both enabled
        if self.show_info and self.show_warnings: # If both warning and info enabled
            return True # Return True
        return False # Else return False
    
    def get_info_enabled(self): # Return if info enabled or not
        return self.show_info
    
    def get_warnings_enabled(self): # Return if info enabled or not
        return self.show_warnings


class Client:
    
    ##### -- Init -- #####
    
    def __init__(self, server_ip, port, header=64, format='utf-8'): #  Default: header is 64 bytes long, format is utf-8
        self.SERVER_IP = server_ip # The IP of the host (public IP for non-lan, private IPV4 for lan)
        self.PORT = port # Port
        self.HEADER = header # Size of header before data sent
        self.FORMAT = format # Format of text being sent
        
        self.CLIENT_IP = socket.gethostbyname(socket.gethostname()) # Computer IP (LAN)
        self.ADDR = (self.SERVER_IP, self.PORT) # Server address
        
        self.data = {'commands':[], 'data':""} # Stores the commands and data being sent to server
        self.server_data = "" # Stores the data recieved from the server

        self.do_disconnect = False # Not disconnected
        self.enable_outputs(True) # Outputs active
        
        self.info(f"Server IP: {self.SERVER_IP}") # Prints the IP the server is running on
        self.info(f"Server PORT: {self.PORT}") # Prints the PORT the server is running on
        self.info(f"Client status: Ready") # Prints that client is ready to start
    
    ### -- Client Handling -- ###
    
    def connect(self): # Connect to server
        self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Connects client to INET, streaming data
        self.server_conn.connect(self.ADDR) # Binds connected address to above
        thread = threading.Thread(target=self.handle_server) # Creates a new thread for this specific connection, with handle_server()
        thread.start() # Starts thread
    
    ### -- Server Handling -- ###
    
    def recieve_message(self): # Recieves massage from a client
        client_message_length = self.server_conn.recv(self.HEADER).decode(self.FORMAT) # Waits for message lenght of next message and decodes from format
        
        if client_message_length: # Makes sure that there is a message
            client_message_length = int(client_message_length)
            client_message = self.server_conn.recv(client_message_length).decode(self.FORMAT) # Waits for message and decodes from format
            client_message = self.eval_message(client_message) # Converts data string into dict
            return client_message
        return "" # If no message return nothing
    
    def send_message(self, message): # Send message to a client
        encoded_message = message.encode(self.FORMAT) # Encodes message
        encoded_message_length = len(encoded_message) # Gets encoded message length
        header_message = str(encoded_message_length).encode(self.FORMAT) # Set header message to the string of the lenght and incode with format
        header_message += b' ' * (self.HEADER - len(header_message)) # Adds blanks to the end to make the header_message the right size
        self.server_conn.send(header_message) # Header sends the message length of main message
        self.server_conn.send(encoded_message) # Sends the message in encoded format
    
    def eval_message(self, message): # Changes string recieved to a dict
        try:
            return ast.literal_eval(message) # Converts data string into dict
        except Exception:
            self.warn(f"Error: Unable to eval message recieved") # If error
            return "" # Return empty
    
    def handle_server(self):
        connected = True
        while connected:
            server_message = self.recieve_message() # Waits to recieve message
            
            if server_message: # If message recieved has a value
                for command in server_message['commands']: # Go through every command
                    if command == "disconnect": # If command disconnect
                        self.add_command("disconnect") # Add command to server
                        connected = False # End thread
                        
                self.server_data = server_message['data'] # Store data in its spcific IP                
            
            if self.do_disconnect: # If client disconnecting
                self.add_command("disconnect") # Add command to server
                connected = False # End thread
                print("weitd")
            
            self.info(f"Message: {server_message}") # Prints server message
            
            self.send_message(f"{self.data}") # Sends message data
    
    ### -- Print -- ###
    
    def warn(self, message): # Displays a warning message (ususally errors)
        if self.show_warnings == True: # If warning messages active
            print(f"[CLIENT WARNING] {message}") # Print warning message
                
    def info(self, message): # Displays an informational message
        if self.show_info == True: # If info messages active
            print(f"[CLIENT INFO] {message}") # Print warning message
    
    ##### -- Action -- #####
    
    def disconnect(self): # Disconnect from server
        self.do_disconnect = True # Set disconnect to true
    
    ##### -- Set -- #####
    
    def set_data(self, data): # Set the data being sent
        self.data['data'] = str(data)
        
    def add_command(self, command): # Add a command being sent to clients
        self.data['commands'].append(str(command))
    
    def remove_all_commands(self): # Remove all commands that will be sent to server
        self.data['commands'] = []
    
    def enable_outputs(self, boolean): # Set outputs for warnings and info to active or inactive
        if type(boolean) == bool: # If input bool
            self.show_warnings = boolean # Warnings active/inactive
            self.show_info = boolean # Info active/inactive
        else:
            self.warn(f"Error: Bool {boolean} not valid for setting enable_outputs") # Error as type of input is not bool
        
    def enable_warnings(self, boolean): # Set outputs for warnings to active or inactive
        if type(boolean) == bool: # If input bool
            self.show_warnings = boolean # Warnings active/inactive
        else:
            self.warn(f"Error: Bool {boolean} not valid for setting enable_warnings") # Error as type of input is not bool
        
    def enable_info(self, boolean): # Set outputs for warnings to active or inactive
        if type(boolean) == bool: # If input bool
            self.show_info = boolean # Info active/inactive
        else:
            self.warn(f"Error: Bool {boolean} not valid for setting enable_info") # Error as type of input is not bool
    
    ##### -- Get -- #####
    
    def get_data(self): # Return server data
        return self.data['data']
    
    def get_commands(self): # Return server commands
        return self.data['commands']
    
    def get_client_data(self): # Return client data dict
        return self.client_data
    
    def get_server_ip(self): # Return server IP
        return self.SERVER_IP
    
    def get_server_port(self): # Return server PORT
        return self.PORT
    
    def get_number_of_active_clients(self): # Return number of clients connected to the server
        return self.active_clients
    
    def get_all_outputs_enabled(self): # Return True if warnings and info are both enabled
        if self.show_info and self.show_warnings: # If both warning and info enabled
            return True # Return True
        return False # Else return False
    
    def get_info_enabled(self): # Return if info enabled or not
        return self.show_info
    
    def get_warnings_enabled(self): # Return if info enabled or not
        return self.show_warnings


main_server = Server(5050)
main_server.enable_info(False)
main_server.start()

import time
time.sleep(0.5)

ip = input("IP: ")

client1 = Client(ip, 5050)
client1.enable_info(False)
client1.connect()

time.sleep(5)

client1.disconnect()