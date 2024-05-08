from lakeserver import * # Import all code from lakeserver
import math

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

    print("This is some example code for my server I created using socket. Made by Tequin Lake. \n")
    
    time.sleep(1)

    print("\n---Starting Server---")
    main_server = Server(5050) # Create new server on port 5050
    main_server.start() # Start server

    time.sleep(1)

    print("\n---Create Clients---")
    client1 = Client(main_server.get_ip(), 5050) # Create new clients
    client2 = Client(main_server.get_ip(), 5050)
    client3 = Client(main_server.get_ip(), 5050)

    time.sleep(1)
    
    print("\n---Connect Client1---")
    client1.connect() # Connect client one

    time.sleep(1)

    print("\n---Sending/receiving client data---")
    
    for x in range(12): # Increment x
        client1.set_data(math.factorial(x)) # Set client data to factorial of x
        print("Server data:", main_server.get_client_data()) # Display server data for all clients
        time.sleep(0.4)

    time.sleep(1)

    print("\n---Disconnecting clients and shutting down server---")
    main_server.shutdown() # Disconnect all clients, and close server
    
    time.sleep(1)

    print("\n---Restarting server---")
    main_server.start() # Start server
    
    time.sleep(1)

    print("\n---Connecting 3 clients---")    
    client1.connect() # Connect all clients
    client2.connect()
    client3.connect()
    
    time.sleep(1)

    print("\n---Display server data---")    
    print("Server data:", main_server.get_client_data()) # Display server data for all clients
    
    time.sleep(0.1)

    print("\n---Client1 disconnects---")    
    client1.disconnect() # Disconnect client one
    
    time.sleep(0.1)

    print("\n---Display updated server data---")    
    print("Server data:", main_server.get_client_data()) # Display server data for all clients
    
    time.sleep(1)
    
    print("\n---Example error: Attempted to start running server---")
    main_server.start() # Server already started, so will cause error (example)
    
    time.sleep(1)

    print("\n---Disable [INFO] and [WARNING] messages---")
    main_server.enable_outputs(False) # Stop any [INFO] and [WARNING] tags from appearing
    print("Example error output for starting server: ")
    main_server.start() # Server already started, so will cause error (example), will not show
    
    print("\n---Enable [INFO] and [WARNING] messages---")
    main_server.enable_info(True) # Allow [INFO] tags to appear, do not effect [WARNING] tags
    
    time.sleep(1)
    print("\n---Disconnecting all clients and shutting down server---")
    main_server.shutdown() # Shutdown server
    
    time.sleep(1)
    input("\nPress Enter to close...") # Wait for user to close window
    
    
if __name__ == "__main__": # Fancy code
    main()