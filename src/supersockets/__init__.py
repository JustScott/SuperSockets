'''
Module to simplify the process of creating servers and clients, with seamless built in encryption options

Classes:
    connect(self, ip:str, port:int, connection_type:str, key=None, RSA=None, socket_timeout=3)
        Class for easily creating socket connections, with built in encryption options. It's pointless
        to set the RSA parameter when connection_type='client', since the server decides whether or not to use RSA.

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

'''

from supersockets.supersockets import connect
