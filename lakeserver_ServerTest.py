import socket, threading, ast # Imports for client and server

class SockStreamConnection:
    
    ##### -- Global Variables -- #####
    
    screen_lock = threading.Semaphore(value=1) # Forces text to be printed at different times
    
    ##### -- Message Handling -- #####
    
    def eval_message(self, message): # Changes string recieved to a dict
        try:
            return ast.literal_eval(message) # Converts data string into dict
        except Exception:
            self.warn(f"Error: Unable to eval message recieved") # If error
            return "" # Return empty

    ### -- Print -- ###
    
    def warn(self, message): # Displays a warning message (ususally errors)
        if self.show_warnings == True: # If warning messages active
            self.screen_lock.acquire() # Gain control over printing text
            print(f"[{self.__class__.__name__} WARNING] {message}") # Print warning message
            self.screen_lock.release() # Release control over printing text
                
    def info(self, message): # Displays an informational message
        if self.show_info == True: # If info messages active
            self.screen_lock.acquire() # Gain control over printing text
            print(f"[{self.__class__.__name__} INFO] {message}") # Print warning message
            self.screen_lock.release() # Release control over printing text
    
    ### -- Set -- ###
    
    def set_data(self, data): # Set the data being sent
        self.data['data'] = str(data)
        
    def add_command(self, command): # Add a command being sent
        self.data['commands'].append(str(command))
    
    def remove_all_commands(self): # Remove all commands that will be sent
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
    
    ### -- Get -- ###
    
    def get_data(self): # Return server data
        return self.data['data']
    
    def get_client_data(self): # Return client data dict
        return self.client_data
    
    def get_all_outputs_enabled(self): # Return True if warnings and info are both enabled
        if self.show_info and self.show_warnings: # If both warning and info enabled
            return True # Return True
        return False # Else return False
    
    def get_info_enabled(self): # Return if info enabled or not
        return self.show_info
    
    def get_warnings_enabled(self): # Return if info enabled or not
        return self.show_warnings
    
    
class Server(SockStreamConnection):
    
    ##### -- Init -- #####
    
    def __init__(self, port, outputs_enabled=True, header=64, format='utf-8'): #  Default: header is 64 bytes long, format is utf-8
        self.PORT = port # Port
        self.HEADER = header # Size of header before data sent
        self.FORMAT = format # Format of text being sent
        
        self.SERVER_IP = socket.gethostbyname(socket.gethostname()) # Computer IP (LAN)
        self.ADDR = (self.SERVER_IP, self.PORT) #Server address
        
        self.active = False # Server currently not active
        
        self.enable_outputs(outputs_enabled) # Outputs active
        
    ##### -- Server Handling -- #####
    
    def start(self, start_accept_clients=True):
        if not self.active:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates server on "INET", and sock stream means we are streaming data
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allows server to be reused after shutdown
            self.server.bind(self.ADDR) # Binds address to server
            
            self.data = {'commands':[], 'data':""} # Stores the commands and data that will be sent to all computers
            self.client_data = {} # Stores the data recieved from every connection
            self.active_clients = 0 # Number of active client connections
            
            self.active = True # Server currently active
            self.do_shutdown = False # Set shutdown to False
            self.accepting_clients = False # Not accepting clients
            
            self.info(f"Server IP: {self.SERVER_IP}") # Prints the IP the server is running on
            self.info(f"Server PORT: {self.PORT}") # Prints the PORT the server is running on
            self.info(f"Status: Ready") # Prints that server is ready to start
            
            if start_accept_clients:
                self.accept_clients() # Starts accepting clients to join server
        
        else:
            self.warn(f"Error: Server is currently active, shutdown the server before starting")
    
    def accept_clients(self):
        if not self.do_shutdown and not self.accepting_clients: # If server not shutting down and server not accepting clients
            self.connection_handler_thread = threading.Thread(target=self.connection_handler) # Creates a new thread for this specific connection, with handle_client()
            self.connection_handler_thread.start() # Starts thread
        elif self.shutdown:
            self.warn(f"Error: Cannot accept clients because server is shutting down") # Error
        else:
            self.warn(f"Error: Cannot accept clients because server is already accepting clients") # Error
    
    def connection_handler(self):
        self.server.listen() # Activates server, and will listen for pings
        
        self.info(f"New Connections: Allow") # Prints that server is active
        
        while True: # Continually adds new connections
            try:
                client_conn, client_addr = self.server.accept() # Waits for a new connection to join the server and gets IP
            except OSError: # If server.accept() raised error because server closed
                break # Exit connection handler
            
            thread = threading.Thread(target=self.handle_client, args=(client_conn, client_addr)) # Creates a new thread for this specific connection, with handle_client()
            thread.start() # Starts thread
            
            self.active_clients += 1 # One more active connection
            
            self.info(f"Active Clients: {self.active_clients}") # Prints how many connections we have on the server
        
        self.info(f"New Connections: Deny") # Print that connection handler shutdown
    
    def handle_shutdown(self):
        while True: # Loop forever
            if self.active_clients == 0: # If no more clients connected
                self.server.close() # Close server
                self.active = False # Server closed
                
                break # End thread
        
        self.info(f"Status: Shutdown") # Server shutdown
    
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
    
    def handle_client(self, client_conn, client_addr): # Given a thread for each connection, gets the clients IP
        self.client_data[client_addr] = "" # Adds this client to the client_data list with no data
        
        connected = True
        while connected:
            if self.do_shutdown: # If server shutting down
                self.add_command("disconnect") # Add command to data
                connected = False # End thread
            
            self.send_message(f"{self.data}", client_conn) # Sends message with server data
            
            client_message = self.recieve_message(client_conn) # Runs recieve message function, and gets message
            
            if client_message: # If message recieved has a value
                for command in client_message['commands']: # Go through every command
                    if command == "disconnect": # If command disconnect
                        connected = False # End thread
                        
                self.client_data[client_addr] = client_message['data'] # Store data in its spcific IP                
        
        del self.client_data[client_addr] # Remove persons data from server data
        self.active_clients -= 1 # Remove one number from active connections
        
        self.info(f"Active Clients: {self.active_clients}") # Prints how many connections we have on the server
        
        client_conn.close() # Closes the connection between the client
    
    ##### -- Action -- #####
    
    def shutdown(self): # Disconnect clients and shutdown server
        self.do_shutdown = True # Set shutdown to true
        
        self.info(f"Status: Starting Shutdown") # Prints message letting user know shutdown has started
        
        thread = threading.Thread(target=self.handle_shutdown) # Creates a new thread for this specific connection, with handle_client()
        thread.start() # Starts thread
    
    ##### -- Get -- #####
    
    def get_commands(self): # Return server commands
        return self.data
    
    def get_ip(self): # Return server IP
        return self.SERVER_IP
    
    def get_port(self): # Return server PORT
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


class Client(SockStreamConnection):
    
    ##### -- Init -- #####
    
    def __init__(self, server_ip, port, outputs_enabled=True, header=64, format='utf-8'): #  Default: header is 64 bytes long, format is utf-8
        self.SERVER_IP = server_ip # The IP of the host (public IP for non-lan, private IPV4 for lan)
        self.PORT = port # Port
        self.HEADER = header # Size of header before data sent
        self.FORMAT = format # Format of text being sent
        
        self.CLIENT_IP = socket.gethostbyname(socket.gethostname()) # Computer IP (LAN)
        self.ADDR = (self.SERVER_IP, self.PORT) # Server address
        
        self.data = {'commands':[], 'data':""} # Stores the commands and data being sent to server
        self.server_data = "" # Stores the data recieved from the server

        self.active = False # Client not connected
        self.do_disconnect = False # Not disconnected
        self.enable_outputs(outputs_enabled) # Outputs active
        
        self.info(f"Status: Ready") # Prints that client is ready to start
    
    ### -- Client Handling -- ###
    
    def connect(self): # Connect to server
        if not self.active: # If not already connected
            self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Connects client to INET, streaming data
            self.server_conn.connect(self.ADDR) # Binds connected address to above
            
            self.data = {'commands':[], 'data':""} # Stores the commands and data being sent to server
            self.server_data = "" # Stores the data recieved from the server

            self.active = True # Connected to server
            self.do_disconnect = False # Not disconnected
            
            self.info(f"Status: Connected") # Prints connected to server
            
            thread = threading.Thread(target=self.handle_server) # Creates a new thread for this specific connection, with handle_server()
            thread.start() # Starts thread
        else:
            self.warn(f"Error: Cannot initiate a connection because client already connected") # Error
    
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
    
    def handle_server(self):
        connected = True
        while connected:
            server_message = self.recieve_message() # Waits to recieve message
            
            if server_message: # If message recieved has a value
                for command in server_message['commands']: # Go through every command
                    if command == "disconnect": # If command disconnect
                        self.add_command("disconnect") # Add command sending to server
                        connected = False # End thread
                        
                        self.info(f"Status: Disconnecting") # Print client is disconnecting
                        
                self.server_data = server_message['data'] # Store data in its spcific IP                
            
            if self.do_disconnect: # If client disconnecting
                self.add_command("disconnect") # Add command to server
                connected = False # End thread
                
                self.info(f"Status: Disconnecting") # Print client is disconnecting
            
            self.send_message(f"{self.data}") # Sends message data
        
        self.active = False # Disconnected
        self.info(f"Status: Disconnected") # Print client has disconnected
    
    ##### -- Action -- #####
    
    def disconnect(self): # Disconnect from server
        self.do_disconnect = True # Set disconnect to true
    
    ##### -- Get -- #####
    
    def get_commands(self): # Return server commands
        return self.data['commands']
    
    def get_ip(self): # Return client IP
        return self.CLIENT_IP
    
    def get_server_ip(self): # Return server IP
        return self.SERVER_IP
    
    def get_server_port(self): # Return server PORT
        return self.PORT
    
    def get_number_of_active_clients(self): # Return number of clients connected to the server
        return self.active_clients


def main():
    import time
    
    print("""\n
  #####                                        #######                     
 #     # ###### #####  #    # ###### #####        #    ######  ####  ##### 
 #       #      #    # #    # #      #    #       #    #      #        #   
  #####  #####  #    # #    # #####  #    #       #    #####   ####    #   
       # #      #####  #    # #      #####        #    #           #   #   
 #     # #      #   #   #  #  #      #   #        #    #      #    #   #   
  #####  ###### #    #   ##   ###### #    #       #    ######  ####    #   \n""")

    print("This is example python code for my server I created using socket. Made by Tequin Lake. \n\n")
    
    time.sleep(1)

    main_server = Server(5050) # Create new server on port 5050
    main_server.start() # Start server

    time.sleep(1)

    client1 = Client(main_server.get_ip(), 5050) # Create new clients
    client2 = Client(main_server.get_ip(), 5050)
    client3 = Client(main_server.get_ip(), 5050)
    
    client1.connect() # Connect client one

    time.sleep(1)
    print("\n")
    
    for x in range(12): # Increment x
        client1.set_data(x) # Set client data to x
        print("Server data:", main_server.get_client_data()) # Display server data for all clients
        time.sleep(0.2)

    time.sleep(1)
    print("\n")

    main_server.shutdown() # Disconnect all clients, and close server
    
    time.sleep(1)
    print("\n")
    
    main_server.start() # Start server
    
    time.sleep(1)
    print("\n")
    
    client1.connect() # Connect all clients
    client2.connect()
    client3.connect()
    
    time.sleep(1)
    print("\n")
    
    print("Server data:", main_server.get_client_data()) # Display server data for all clients
    
    time.sleep(0.1)
    
    client1.disconnect() # Disconnect client one
    
    time.sleep(0.1)
    
    print("Server data:", main_server.get_client_data()) # Display server data for all clients
    
    time.sleep(1)
    print("\n")
    
    print("Example error: ", end='')
    main_server.start() # Server already started, so will cause error (example)
    
    time.sleep(1)
    print("\n")
    
    main_server.enable_outputs(False) # Stop any [INFO] and [WARNING] tags from appearing
    print("Example error blocked: ", end='')
    main_server.start() # Server already started, so will cause error (example), will not show
    
    main_server.enable_info(True) # Allow [INFO] tags to appear, do not effect [WARNING] tags
    
    time.sleep(1)
    print("\n\n")
    
    main_server.shutdown() # Shutdown server
    
    
    time.sleep(1)
    print("\n")
    input("Press Enter to close window...") # Wait for user to close window
    
    
if __name__ == "__main__": # Fancy code
    main()