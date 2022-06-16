from lakeserver import * # Import all code from lakeserver

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