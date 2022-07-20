'''
Module to simplify the process of creating servers and clients, with seamless built in encryption options

Classes:
    server()
        Used to create a server connection that the client class can interact
        with using the send() and recv() methods.
    
        __init__(self, ip:str, port:int, key=None, RSA=False, socket_timeout=.5)

        Methods:
            create_secure_connection(self, rsa_enabled: bool) -> bool
                Uses RSA cryptography to automatically share a key between the server and client,
                for use in symmetric encryption for any future messages
            send(self, data: any) -> bool
                Sends the data
            recv() -> any
                Ensures successful receival of data sent from the 'send' method            
            
            __del__(self) -> bool
                Automatically closes the connection between the 
                client and server upon the programs end.

    client(server)
        Used to connect to an active server created by the server class,
        interactions can be made using the send() and recv() methods.
    
        __init__(self, ip:str, port:int, key=None, socket_timeout=.5)
    
        Methods:
            create_secure_connection(self) -> bool:
                Uses RSA cryptography to share a symmetric key between the server and client,
                for use in symmetric encryption for future messages

            Inherits:
                send, recv, __del__

'''

from supersockets.supersockets import server,client
