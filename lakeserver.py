##### -- Imports -- #####
import socket, threading, ast # Imports for client and server

class SockStreamConnection:
    
    ##### -- Global Variables -- #####
    
    screen_lock = threading.Semaphore(value=1)
    
    ##### -- Message Handling -- #####
    
    @classmethod
    def do_nothing():
        pass

    def eval_message(self, message):
        """
        Safely return the eval of a string.
        
        The function attempts to safely return the eval of a string with ast.literal_eval. If the string can not be evaled due to a ValueError then call self.warn and return None.
        
        This is useful for converting the string with a dictionary inside to just a dictionary, without causing any security risks.
    
        Parameters
        ----------
        message : string
            A evaluable string.

        Returns
        -------
        any
            The result of the evaled string.
            
        ** ValueError **
        If string cannot be evaled due to ValueError raised:
        
        NoneType
            None.
            
        Examples
        --------
        >>> message = SockStreamConnection.eval_message("{'one':1, 'two':2, 'three':3}")
        >>> print(message)
        {'one':1, 'two':2, 'three':3}

        ** ValueError **
        If string cannot be evaled due to ValueError raised:
        
        >>> message = SockStreamConnection.eval_message("{'one':1, 'two':2, 'three':3}")
        [SockStreamConnection WARNING] Error: Unable to eval message recieved
        >>> print(message)
        None
        """
        if type(message) == str and message:
            try:
                return ast.literal_eval(message)
            except ValueError:
                self.warn("Error: Unable to eval message recieved")
        return None

    def post_recieve_update(self, message): # Runs the function for after recieved a message, needs to take the message variable, and return final changed data
        """
        Execute the post recieve function.
        
        Executes the post recieve function if it is callable. The post recieve function takes the variable 'message' when run. Any errors the function throws are caught, then calls self.warn with the error. The post recieve function returns a new message which is then returned.
        
        This is useful to run after recieving a message a connection has sent to the receiver, to easily and repetively change the message recieved.
        
        Parameters
        ----------
        message : string
            The message recieved that will be changed

        Returns
        -------
        any
            The final changed message outputed by the post recieve function
            
        ** Exception **
        If if the post recieve function raises an error:
        
        message : any
            The origional message before changes
            
        Examples
        --------
        >>> import lakeserver
        >>> main_server = lakeserver.Server(5050)
        >>> def my_func(class_self, message):
        ...     return message.strip()
        >>> main_server.set_post_recieve_func(my_func)
        >>> message_recieved = "Hello World  "
        >>> main_server.post_recieve_update(message_recieved)
        'Hello World'

        ** Exception **
        If if the post recieve function raises an error:
        
        >>> import lakeserver
        >>> def my_func(class_self, message):
        ...     raise Exception("An Error")
        >>> main_server.set_post_recieve_func(my_func)
        >>> message_recieved = "Hello World  "
        >>> main_server.post_recieve_update(message_recieved)
        [Server WARNING] Error: Post recieve function 'my_func' returned the error 'An Error'
        'Hello World  '
        """
        if callable(self.post_recieve_func):
            try:
                return self.post_recieve_func(self, message)
            except Exception as e:
                self.warn(f"Error: Post recieve function '{self.post_recieve_func.__name__}' returned the error '{e}'")
                return message
            
        #self.warn(f"Error: Post recieve function is not callable")
        return message
        
    def pre_send_update(self): # Runs the function for before sending a messgae
        if callable(self.pre_send_func): # If variable a function
            try:
                self.pre_send_func(self) # Run function
            except Exception as e:
                self.warn(f"Error: Pre send function {self.post_recieve_func.__name__} returned the error {e}") # Error
    
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
    
    def set_post_recieve_func(self, func): # Set post_recieve_func to a function
        if callable(func): # If a function
            self.post_recieve_func = func # Set to function
        else:
            self.warn("Error: Variable supplied for was not a function") # Error
    
    def remove_post_recieve_func(self): # Remove post_recieve_func
        self.post_recieve_func = None # Set to None
        
    def set_pre_send_func(self, func): # Set pre_send_func to a function
        if callable(func): # If a function
            self.pre_send_func = func # Set to function
        else:
            self.warn("Error: Variable supplied for was not a function") # Error
    
    def remove_pre_send_func(self): # Remove pre_send_func
        self.pre_send_func = None # Set to None
    
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
    
    def get_all_outputs_enabled(self): # Return True if warnings and info are both enabled
        return bool(self.show_info and self.show_warnings)
    
    def get_info_enabled(self): # Return if info enabled or not
        return self.show_info
    
    def get_warnings_enabled(self): # Return if info enabled or not
        return self.show_warnings
    
    
class Server(SockStreamConnection):
    
    ##### -- Init -- #####
    
    def __init__(self, port, direct=False, outputs_enabled=True, header=64, format='utf-8', pre_send_func=None, post_recieve_func=None): #  Default: header is 64 bytes long, format is utf-8, no functions
        self.PORT = port # Port
        self.HEADER = header # Size of header before data sent
        self.FORMAT = format # Format of text being sent
        self.DIRECT = direct # Is direct
        
        self.SERVER_IP = socket.gethostbyname(socket.gethostname()) # Computer IP (LAN)
        self.ADDR = (self.SERVER_IP, self.PORT) #Server address
        
        self.pre_send_func = pre_send_func # By default no function being run before send
        self.post_recieve_func = post_recieve_func # By default no function being run after recieve
        
        self.data = {'commands':[], 'data':""} # Stores the commands and data that will be sent to all computers
        self.client_conn = {} # Stores all connections of clients
        self.client_data = {} # Stores the data recieved from every connection
        self.active_clients = 0 # Number of active client connections
        
        self.active = False # Server currently not active
        self.do_shutdown = False # Set shutdown to False
        self.accepting_clients = False # Not accepting clients
        
        self.enable_outputs(outputs_enabled) # Outputs active
        
    ##### -- Server Handling -- #####
    
    def start(self, start=True):
        if not self.active and self.server_addr_avalible(): # Check if server not active and not connected
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates server on "INET", and sock stream means we are streaming data
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allows server to be reused after shutdown
            self.server.bind(self.ADDR) # Binds address to server
            
            self.data = {'commands':[], 'data':""} # Stores the commands and data that will be sent to all computers
            self.client_conn = {} # Stores all connections of clients
            self.client_data = {} # Stores the data recieved from every connection
            self.active_clients = 0 # Number of active client connections
            
            self.active = True # Server currently active
            self.do_shutdown = False # Set shutdown to False
            self.accepting_clients = False # Not accepting clients
            
            self.info(f"Server IP: {self.SERVER_IP}") # Prints the IP the server is running on
            self.info(f"Server PORT: {self.PORT}") # Prints the PORT the server is running on
            self.info(f"Status: Ready") # Prints that server is ready to start
            
            if start:
                self.accept_clients(self.DIRECT)
        else:
            if self.active:
                self.warn(f"Error: Server is currently active, shutdown the server before starting")
            else:
                self.warn(f"Error: Server is currently active in other code on computer, shutdown the other server before starting")
    
    def accept_clients(self, direct):
        if not self.do_shutdown and not self.accepting_clients: # If server not shutting down and server not accepting clients
            self.connection_handler_thread = threading.Thread(target=self.connection_handler, args=(direct, )) # Creates a new thread for this specific connection, with handle_client_echo()
            self.connection_handler_thread.daemon = True  # Dies when main thread (only non-daemon thread) exits
            self.connection_handler_thread.start() # Starts thread
        elif self.shutdown:
            self.warn("Error: Cannot accept clients because server is shutting down") # Error
        else:
            self.warn("Error: Cannot accept clients because server is already accepting clients") # Error
    
    def connection_handler(self, direct):
        self.server.listen() # Activates server, and will listen for pings
        
        self.info(f"New Connections: Allow") # Prints that server is active
        
        while True: # Continually adds new connections
            try:
                client_conn, client_addr = self.server.accept() # Waits for a new connection to join the server and gets IP
            except OSError: # If server.accept() raised error because server closed
                break # Exit connection handler
            
            if direct:
                thread = threading.Thread(target=self.handle_client_direct, args=(client_conn, client_addr)) # Creates a new thread for this specific connection, with handle_client_direct()
            else:
                thread = threading.Thread(target=self.handle_client_echo, args=(client_conn, client_addr)) # Creates a new thread for this specific connection, with handle_client_echo()
            
            thread.daemon = True  # Dies when main thread (only non-daemon thread) exits
            thread.start() # Starts thread
            
            self.active_clients += 1 # One more active connection
            
            self.info(f"Client Event: Connected") # Prints client =connected
        
        self.info(f"New Connections: Deny") # Print that connection handler shutdown
    
    def handle_shutdown(self):
        if self.active:
            self.info("Status: Starting Shutdown") # Server shutdown
            while True: # Loop forever
                if self.active_clients == 0: # If no more clients connected
                    self.server.close() # Close server
                    self.active = False # Server closed
                    
                    break # End thread
            
            self.info("Status: Shutdown") # Server shutdown
        else:
            self.warn("Error: Could not shutdown server as it is not online") # Error
    
    def server_addr_avalible(self): # Check if ip and port is already connected to a server
        try: # Will cause error if no external server
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates server on "INET", and sock stream means we are streaming data
            server.connect(self.ADDR) # Connect to other server
            return False
        except ConnectionRefusedError: # Could not find server (good)
            return True
    
    ##### -- Client Handling -- #####
    
    def direct_recieve(self, client_conn): # Recieve message from a client
        recv_length = 0
        data = ""
        
        while self.HEADER - recv_length > 0:
            recv_data = client_conn.recv(self.HEADER - recv_length).decode(self.FORMAT)
            data += recv_data
            recv_length = len(data)
        
        return self.eval_message(data) # Waits for message and decodes from format, then evals
    
    def direct_send(self, client_conn, message): # Send a client connected with direct a message
        try: # Can cause error
            self.pre_send_update() # Handle server data with function

            message = "{'commands':" + str(self.get_commands()) + ", 'data':" + str(message) + "}" # Format message for data
            
            encoded_message = message.encode(self.FORMAT) # Encodes message
            encoded_message += b' ' * (self.HEADER - len(encoded_message)) # Adds blanks to the end to make the encoded_message the right size
            client_conn.send(encoded_message) # Sends the message in encoded format
        except ConnectionResetError: # If trying to send/recieve message returns it is not active
            pass
        except ConnectionAbortedError: # If trying to send/recieve message returns it is not active
            pass
        
    def direct_send_all(self, message): # Send all clients connected with direct a message
        attempting = True
        while attempting:
            try: 
                for connection in self.client_conn.values(): # For each connection
                    self.direct_send(connection, message) # Send message
                attempting = False
            except RuntimeError:
                pass
    
    def handle_client_direct(self, client_conn, client_addr): # Given a thread for each connection, gets the clients IP, directly messages client
        self.client_data[client_addr] = "" # Adds this client to the client_data list with no data
        self.client_conn[client_addr] = client_conn # Stores connection of client
        
        client_message = ""
        connected = True
        while connected:
            if self.do_shutdown: # If server shutting down
                connected = False # End thread
            
            try: # Can cause error
                client_message = self.direct_recieve(client_conn) # Recieve
            except ConnectionResetError: # If trying to send/recieve message returns it is not active
                self.warn("Error: Client disconnected without commanding disconnect, can not recieve message. Disconnecting client.") # Error
                connected = False # End thread
            except ConnectionAbortedError: # If trying to send/recieve message returns it is not active
                self.warn("Error: Client disconnected without commanding disconnect, can not recieve message. Disconnecting client.") # Error
                connected = False # End thread
            
            if client_message: # If message recieved has a value
                client_message = self.post_recieve_update(client_message) # Handle client messsage with function
                
                for command in client_message['commands']: # Go through every command
                    if command == "disconnect": # If command disconnect
                        connected = False # End thread
                        
                self.client_data[client_addr] = client_message['data'] # Store data in its spcific IP                
        
        del self.client_conn[client_addr] # Remove clients conn from data
        del self.client_data[client_addr] # Remove persons data from server data
        self.active_clients -= 1 # Remove one number from active connections
        
        self.info(f"Client Event: Disconnected") # Prints client disconnected
        
        client_conn.close() # Closes the connection between the client
    
    def recieve_message(self, client_conn): # Recieves message from a client
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
        
        try:
            client_conn.send(header_message) # Header sends the message length of main message
            client_conn.send(encoded_message) # Sends the message in encoded format
        except BrokenPipeError:
            self.warn("Error: Message send failed - lost connection to server")

    def handle_client_echo(self, client_conn, client_addr): # Given a thread for each connection, gets the clients IP, messages client through echos
        self.client_data[client_addr] = "" # Adds this client to the client_data list with no data
        self.client_conn[client_addr] = client_conn # Stores connection of client
        
        client_message = ""
        connected = True
        while connected:
            if self.do_shutdown: # If server shutting down
                self.add_command("disconnect") # Add command to data
                connected = False # End thread
            
            self.pre_send_update() # Handle server data with function
            
            try: # Can cause error
                self.send_message(f"{self.data}", client_conn) # Sends message with server data
                client_message = self.recieve_message(client_conn) # Runs recieve message function, and gets message
            except ConnectionResetError: # If trying to send/recieve message returns it is not active
                self.warn("Error: Client disconnected without commanding disconnect. Disconnecting client.") # Error
                connected = False # End thread
            except ConnectionAbortedError: # If trying to send/recieve message returns it is not active
                self.warn("Error: Client disconnected without commanding disconnect. Disconnecting client.") # Error
                connected = False # End thread
            
            if client_message: # If message recieved has a value
                client_message = self.post_recieve_update(client_message) # Handle client messsage with function
                
                for command in client_message['commands']: # Go through every command
                    if command == "disconnect": # If command disconnect
                        connected = False # End thread
                        
                self.client_data[client_addr] = client_message['data'] # Store data in its spcific IP                
        
        del self.client_conn[client_addr] # Remove clients conn from data
        del self.client_data[client_addr] # Remove persons data from server data
        self.active_clients -= 1 # Remove one number from active connections
        
        self.info("Client Event: Disconnected") # Prints client disconnected
        
        client_conn.close() # Closes the connection between the client
    
    ##### -- Action -- #####
    
    def shutdown(self): # Disconnect clients and shutdown server
        self.do_shutdown = True # Set shutdown to true
        self.add_command("disconnect") # Add command to data
        
        thread = threading.Thread(target=self.handle_shutdown) # Creates a new thread for this specific connection, with handle_client_echo()
        thread.daemon = True  # Dies when main thread (only non-daemon thread) exits
        thread.start() # Starts thread
    
    ##### -- Get -- #####
    
    def get_commands(self): # Return server commands
        return self.data["commands"]
    
    def get_client_data(self): # Return client data dict
        return self.client_data
    
    def get_ip(self): # Return server IP
        return self.SERVER_IP
    
    def get_port(self): # Return server PORT
        return self.PORT
    
    def get_number_of_active_clients(self): # Return number of clients connected to the server
        return self.active_clients


class Client(SockStreamConnection):
    
    ##### -- Init -- #####
    
    def __init__(self, server_ip, port, direct=False, outputs_enabled=True, header=64, format='utf-8', pre_send_func=None, post_recieve_func=None): #  Default: header is 64 bytes long, format is utf-8, no functions
        self.SERVER_IP = server_ip # The IP of the host (public IP for non-lan, private IPV4 for lan)
        self.PORT = port # Port
        self.HEADER = header # Size of header before data sent
        self.FORMAT = format # Format of text being sent
        self.DIRECT = direct # Is direct
        
        self.CLIENT_IP = socket.gethostbyname(socket.gethostname()) # Computer IP (LAN)
        self.ADDR = (self.SERVER_IP, self.PORT) # Server address
        
        self.pre_send_func = pre_send_func # By default no function being run before send
        self.post_recieve_func = post_recieve_func # By default no function being run after recieve
        
        self.data = {'commands':[], 'data':""} # Stores the commands and data being sent to server
        self.server_data = {} # Stores the data recieved from the server

        self.active = False # Client not connected
        self.do_disconnect = False # Not disconnected
        self.enable_outputs(outputs_enabled) # Outputs active
        
        self.info("Status: Ready") # Prints that client is ready to start
    
    ### -- Client Handling -- ###
    
    def connect(self): # Connect to server
        if not self.active: # If not already connected
            self.server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Connects client to INET, streaming data
            
            connected_to_server = False # Before trying to connect to server
            try:
                self.server_conn.connect(self.ADDR) # Binds connected address to above
                connected_to_server = True # Managed to connect to server
            except ConnectionRefusedError: # Could not connect to server as it will not accept client
                self.warn("Error: Could not connect to server as it is not accepting clients") # Error
            except TimeoutError: # Server does not exist
                self.warn("Error: Could not connect to server as it does not exist") # Error
            except socket.gaierror: # Weird error - not address
                self.warn("Error: Could not connect to server as address supplied is not valid") # Error
            
            if connected_to_server:
                self.data = {'commands':[], 'data':""} # Stores the commands and data being sent to server
                self.server_data = {} # Stores the data recieved from the server

                self.active = True # Connected to server
                self.do_disconnect = False # Not disconnected
                
                self.info("Status: Connected") # Prints connected to server
                
                if self.DIRECT:
                    thread = threading.Thread(target=self.handle_server_direct) # Creates a new thread for this specific connection, with handle_server_direct()
                else:
                    thread = threading.Thread(target=self.handle_server_echo) # Creates a new thread for this specific connection, with handle_server_echo()
                
                thread.daemon = True  # Dies when main thread (only non-daemon thread) exits
                thread.start() # Starts thread
        else:
            self.warn("Error: Cannot initiate a connection because client already connected") # Error
    
    ### -- Server Handling -- ###
    
    def direct_recieve(self): # Recieves message from a client
        recv_length = 0
        data = ""
        
        while self.HEADER - recv_length > 0:
            recv_data = self.server_conn.recv(self.HEADER - recv_length).decode(self.FORMAT)
            data += recv_data
            recv_length = len(data)
        
        return self.eval_message(data) # Waits for message and decodes from format, then evals
    
    def direct_send(self, message): # Send message to a client
        self.pre_send_update() # Handle server data with function
        
        message = "{'commands':" + str(self.get_commands()) + ", 'data':" + str(message) + "}" # Format message for data
        
        try: # Recieve can cause error
            encoded_message = message.encode(self.FORMAT) # Encodes message
            encoded_message += b' ' * (self.HEADER - len(encoded_message)) # Adds blanks to the end to make the encoded_message the right size
            self.server_conn.send(encoded_message) # Sends the message in encoded format
        except ConnectionResetError: # If trying to recieve message returns it is not active
            pass

    def handle_server_direct(self):
        server_message = ""
        connected = True
        while connected:
            try: # Recieve can cause error
                server_message = self.direct_recieve() # Waits to recieve message
            except ConnectionResetError: # If trying to recieve message returns it is not active
                self.warn("Error: Server disconnected without commanding disconnect, can not recieve message. Disconnecting client.") # Error
                self.info("Status: Disconnecting") # Print client is disconnecting
                break # Leave loop
            
            if server_message: # If message recieved has a value
                server_message = self.post_recieve_update(server_message) # Handle server messsage with function
                
                for command in server_message['commands']: # Go through every command
                    if command == "disconnect": # If command disconnect
                        self.do_disconnect = True # Disconnect
                        
                self.server_data = server_message['data'] # Store server data as a dict
            
            if self.do_disconnect: # If client disconnecting
                connected = False # End thread
                
                self.info("Status: Disconnecting") # Print client is disconnecting
        
        self.active = False # Disconnected
        self.info("Status: Disconnected") # Print client has disconnected
    
    def recieve_message(self): # Recieves message from a client
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
    
    def handle_server_echo(self):
        server_message = ""
        connected = True
        while connected:
            try: # Recieve can cause error
                server_message = self.recieve_message() # Waits to recieve message
            except ConnectionResetError: # If trying to recieve message returns it is not active
                self.warn("Error: Server disconnected without commanding disconnect. Disconnecting client.") # Error
                break # Leave loop
            
            if server_message: # If message recieved has a value
                server_message = self.post_recieve_update(server_message) # Handle server messsage with function
                
                for command in server_message['commands']: # Go through every command
                    if command == "disconnect": # If command disconnect
                        self.do_disconnect = True # Disconnect
                        
                self.server_data = self.eval_message(server_message['data']) # Store server data as a dict
            
            if self.do_disconnect: # If client disconnecting
                connected = False # End thread
                
                self.info("Status: Disconnecting") # Print client is disconnecting
            
            self.pre_send_update() # Handle server data with function
            
            try: # Send can cause error
                self.send_message(f"{self.data}") # Sends message data
            except ConnectionResetError: # If trying to recieve message returns it is not active
                self.warn("Error: Server disconnected without commanding disconnect. Disconnecting client.") # Error
                self.info("Status: Disconnecting") # Print client is disconnecting
                break # Leave loop
        
        self.active = False # Disconnected
        self.info("Status: Disconnected") # Print client has disconnected
    
    ##### -- Action -- #####
    
    def disconnect(self): # Disconnect from server
        self.add_command("disconnect") # Add command to data
        self.do_disconnect = True # Set disconnect to true
    
    ##### -- Get -- #####
    
    def get_server_data(self): # Return server data recieved
        return self.server_data
    
    def get_commands(self): # Return client commands
        return self.data['commands']
    
    def get_ip(self): # Return client IP
        return self.CLIENT_IP
    
    def get_server_ip(self): # Return server IP
        return self.SERVER_IP
    
    def get_server_port(self): # Return server PORT
        return self.PORT