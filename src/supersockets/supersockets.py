'''
Module to simplify the process of creating servers and clients, with seamless built in encryption options

Class:
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
        
        close_connection(self) -> bool
            Close the connection between the client and server. Both sides can use this method.
            This isn't always necessary, but it's good practice to close connections you're no
            longer using

'''


import socket
from listcrypt import encrypt, decrypt, sha256, convert_data, convert_data_back
from rapidrsa import rsa
import json
from time import sleep

class connect:
    '''
    Class for easily creating socket connections, with built in encryption options. It's pointless
    to set the RSA parameter when connection_type='client', since the server decides whether or not to use RSA.
    '''
    def __init__(self, ip:str, port:int, connection_type:str, key=None, RSA=None, socket_timeout=3):
        '''
        method:: __init__(ip, port, connection_type, key=None, RSA=None, socket_timeout=10)

        Args:
            ip (str): Ip Address

            port (int): The Designated Port

            connection_type (str): 
                Either starts the class as a 'server' or a 'client', not case sensitive

            key (str, optional): 
                Used to encrypt/decrypt data sent/received, leave blank to send data in clear text
    
            RSA (bool, optional): 
                Creates an encrypted tunnel between the server and client without you needing to set a password
                on either, just make sure it's enabled on both for it to work

            socket_timeout (int, optional): 
                the time in seconds the socket wait for a connection before closing

        '''
        
        self.server = True
        self.client = False

        # Changes Whether you do the client or server startup process
        if connection_type.lower() == "client":
            self.server = False
            self.client = True

        # Client Startup Process
        if self.client:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                client.connect((ip, port))
            except ConnectionRefusedError:
                try:
                    sleep(.00001) #Allows the server time to reset if reconnecting quickly
                    client.connect((ip,port))
                except ConnectionRefusedError:
                    raise ConnectionRefusedError("Is your server on?")
            client.settimeout(socket_timeout)
            self.con = client
            

        # Server Startup Process
        if self.server:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server.bind((ip, port))
            except PermissionError:
                raise PermissionError(f"Port {port} is already in use by another service, try a port above 999")
            except OSError:
                raise OSError(f"'{ip}' must not be your ip address")
            server.listen()
            self.con, self.address = server.accept()

        self.key = key
        
        self.rsa = rsa

        if RSA:
            self.create_secure_connection(True)
        if not RSA:
            self.create_secure_connection(False)


    def create_secure_connection(self, rsa_enabled: bool):
        '''
        Uses RSA cryptography to automatically share a key between the server and client,
        for use in symmetric encryption for any future messages
        
        :method:: create_secure_connection(self, rsa_enabled: bool) -> bool
                
        Args:
            rsa_enabled (bool):
                Tells the server/client whether to create the secure connection

        Returns:
            True if the everything runs without error
        '''
        if self.server and rsa_enabled:
            rsa = self.rsa
            self.send("rsa enabled")
            self.send(rsa.public_key.decode())
            session_password = rsa.decrypt(self.recv())
            confirmation_message = rsa.generate_password(length=16)
            confirmation_hash = sha256(confirmation_message)
            confirmation_data = {
                "message":encrypt(session_password,confirmation_message),
                "hash":confirmation_hash,
            }
            self.send(confirmation_data)
            if self.recv() == "key confirmed":
                self.key = session_password
        if self.server and not rsa_enabled:
            self.send("rsa disabled")
        
        if self.client:
            rsa_confirmation = self.recv()
            if rsa_confirmation == "rsa enabled":
                public_key = self.recv().encode()
                rsa = self.rsa
                rsa.public_key=public_key
                rsa.private_key = None
                session_password = rsa.generate_password()
                self.send(rsa.encrypt(session_password))
                confirmation_data = self.recv()
                if sha256(decrypt(session_password,confirmation_data["message"])) == confirmation_data["hash"]:
                    self.send("key confirmed")
                    self.key = session_password

        return True


    def send(self, data:any) -> bool:
        '''
        Sends the data 

        :method:: send(self, data: any) -> bool

        Args:
            data (any):
                Any data that you want to send, should accept all data types
        Returns:
            bool:
                True if everything is sent successfully
        '''

        key = self.key
        
        metadata = convert_data('test',data)

        data = {"data":metadata[0],"type":metadata[1]}
        data = json.dumps(data)

        # using 'if key:', so that if a key was given, its used to encrypt the data
        if key:
            '''
            Sending the length of the message/data, to ensure no
            data is lost
            '''
            self.con.send(encrypt(key, str(len(data))))
        if not key:
            self.con.send(str(len(data)).encode("utf-8"))

        #Ensures the size of the data sends without error
        self.con.recv(10)

        if key:
            self.con.send(encrypt(key, data))
        if not key:
            self.con.send(data.encode("utf-8"))


        return True



    def recv(self) -> any:
        '''
        Ensures successful receival of data sent from the 'send' method  
        
        :method:: recv() -> any

        Returns:
            any:
                The data that was sent to you

        '''

        key = self.key

        if key:
            '''
            Receiving the size of the data that will be received
            to make sure its all receieved later in the method
            ''' 
            size = int(decrypt(key, self.con.recv(1024)))
        else:
            size = int(self.con.recv(1024).decode("utf-8"))

        #Ensures the size of the data is received without error
        self.con.send("True".encode())

        data = ""
        '''
        Maximum receivable socket input at once is 65536, if size is greater
        than that we loop through until all of the data is recieved
        '''
        if size < 65536:
            if key:
                data = decrypt(key, self.con.recv(size))
            else:
                data = self.con.recv(size).decode("utf-8")
        if size > 65536:
            while len(data) < size:
                if key:
                    data += decrypt(key, self.con.recv(65536))
                else:
                    data += self.con.recv(65536).decode("utf-8")

        metadata = json.loads(data)

        data = convert_data_back((metadata["data"], metadata["type"]))

        return data

    def close_connection(self) -> bool:
        '''
        Close the connection between the client and server. Both sides can use this method.
        
        :method:: close_connection(self) -> bool

        Returns:
            bool:
                True if the connection is closed successfully
        '''
        self.con.close()

        return True


if __name__=="__main__":
    if False:
        server = connect(ip="0.0.0.0", port="1001", connection_type="server", RSA=True)
        server.send("Can you here me?")
        print(server.recv())
        '''Not required to close the connection, but it's good practice. Only close server connections
        if you don't plan on connecting to any more clients'''
        server.close_connection()        

    if False:
        client = connect(ip="0.0.0.0", port="1001", connection_type="client", RSA=True)
        print(server.recv())
        client.send("Loud and clear!")
        #Not required to close the connection, but it's good practice
        client.close_connection()
