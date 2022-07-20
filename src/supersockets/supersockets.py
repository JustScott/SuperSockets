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


import socket
from listcrypt import encrypt, decrypt, sha256, convert_data, convert_data_back
from rapidrsa import rsa
import json
from time import sleep


class server:
	'''
	Used to create a server connection that the client class can interact
	with using the send() and recv() methods.

	__init__(self, ip:str, port:int, key=None, RSA=False, socket_timeout=.5)

	Args:
            ip (str): 
                Ip Address
            
            port (int): 
                The Designated Port
            
            key (str, optional): 
                Used to encrypt/decrypt data sent/received, leave blank to send data in clear text
    
            RSA (bool, optional): 
                Creates an encrypted tunnel between the server and client without you needing to set a password
                on either, just make sure it's enabled on both for it to work
            
            socket_timeout (int, optional): 
                the time in seconds the socket wait for a connection before closing	
	'''
	def __init__(self, ip:str, port:int, key=None, RSA=False, socket_timeout=.5):
		#Defining socket settings
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		#Sets up the server connection, with helpful error messages for common configuration mistakes
		try:
			server.bind((ip, port))
		except PermissionError:
			raise PermissionError(f"Port {port} is already in use by another service, try a port above 999")
		except OSError:
			raise OSError(f"'{ip}' must not be your ip address")
		
		#Listens for, and opens connections with clients 
		server.listen()
		self.con, self.address = server.accept()
		server.settimeout(socket_timeout)


		self.key = key

		if RSA:
			self.rsa = rsa()

		self.create_secure_connection(RSA)


	def create_secure_connection(self, rsa_enabled: bool):
		'''
		Uses RSA cryptography to share a symmetric key between the server and client,
		for use in symmetric encryption for future messages
		
		:method:: create_secure_connection(self, rsa_enabled: bool) -> bool
				
		Args:
			rsa_enabled (bool):
				Tells the server/client whether to create the secure connection
		Returns:
			True if the everything runs without error
		'''
		if rsa_enabled:
			#Send the public_key to the client
			rsa = self.rsa
			pub_key = rsa.public_key
			self.send(pub_key)

			#Receive the randomly generated symmetric key
			session_password = rsa.decrypt(self.recv())
			#Generate a random string to encrypt and hash as verification of a working symmetric key
			confirmation_data = rsa.generate_password(length=10)
			#Used to confirm that the server received the session_password, and that it works correctly
			symmetric_key_confirmation = {
				"data": encrypt(session_password, confirmation_data),
				"hash": sha256(confirmation_data)
			}
			self.send(symmetric_key_confirmation)
			#If True, both the server and client now have an agreed upon symmetric key
			if self.recv() == confirmation_data:
				self.key = session_password

		if not rsa_enabled:
			self.send("rsa_disabled")
		
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
		#Converting data to suitable format for sending over the network
		metadata = convert_data('test',data)
		data = {"data":metadata[0],"type":metadata[1]}
		data = json.dumps(data)

		'''
		Sends the len of the data first, for a more efficient
		transfer of data	
		'''
		if self.key:
			encrypted_data = encrypt(self.key,data)
			self.con.send((str(len(encrypted_data))+'@').encode())
			self.con.send(encrypted_data)
			return True
   
		self.con.send((str(len(data))+'@').encode())
		self.con.send(data.encode())
		return True


	def recv(self) -> any:
		'''
		Ensures successful receival of data sent from the 'send' method  
		
		:method:: recv(self) -> any
		Returns:
			any:
				The data that was sent to you
		'''
		
		byte = ''
		while True:
			byte += self.con.recv(1).decode()
			if byte[-1] == '@':
				size = int(byte.replace('@',''))
				break
	
		received = b''
		while size > 65536:
			received += self.con.recv(65536)
			size -= 65536

		received += self.con.recv(size)

		if self.key:
			encrypted_data = received
			try:
				data = decrypt(self.key, encrypted_data)
			except Exception:
				raise ValueError('You probably used the wrong decryption key.')
		else:
			data = received.decode()


		#Converting data back to its origional format
		metadata = json.loads(data)
		data = convert_data_back((metadata["data"], metadata["type"]))

		return data


	def __del__(self) -> bool:
		'''
		Automatically closes the connection between the 
		client and server upon the programs end.
		
		:method:: __del__(self) -> bool
		
		Returns:
			bool:
				True if the connection is closed successfully
		'''
		self.con.close()

		return True


class client(server):
	'''
	Used to connect to an active server created by the server class,
	interactions can be made using the send() and recv() methods.
	
	__init__(self, ip:str, port:int, key=None, socket_timeout=.5)

	Args:
            ip (str): 
                Ip Address
            
            port (int): 
                The Designated Port
            
            key (str, optional): 
                Used to encrypt/decrypt data sent/received, leave blank to send data in clear text
    
            socket_timeout (int, optional): 
                the time in seconds the socket wait for a connection before closing
	'''
	def __init__(self, ip:str, port:int, key=None, socket_timeout=.5):
		#Defining socket settings
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		client.settimeout(socket_timeout)

		#Connects to the server, gives some room for connection synchronization errors
		for i in range(5):
			try:
				client.connect((ip, port))
				break
			except Exception:
				if i == 4:
					raise ConnectionRefusedError("Is your server on?")
				sleep(.1)
		

		self.con = client
		self.key = key

		#Set the public_key to a random string so the client doesn't unnecessarily generate its own keys
		self.rsa = rsa(public_key='temporary')

		self.create_secure_connection()


	def create_secure_connection(self) -> bool:
		'''
		Uses RSA cryptography to share a symmetric key between the server and client,
		for use in symmetric encryption for future messages
		
		:method:: create_secure_connection(self) -> bool
				
		Returns:
			True if the everything runs without error
		'''
		#Waits 30 seconds to recieve the public_key from the server, otherwise it raises an error
		received_key = False
		for i in range(30):
			try:
				public_key = self.recv()
				received_key = True
				break
			except socket.timeout:
				pass
			sleep(1)
		if not received_key:
			raise socket.timeout("Waited 30 seconds, but never received the public key from the server")

		if public_key != 'rsa_disabled':
			#Setting the public key
			rsa = self.rsa
			rsa.public_key = public_key
			#Generate and encrypt a random string of characters, and send it to the server
			session_password = rsa.generate_password()
			encrypted_session_password = rsa.encrypt(session_password)
			self.send(encrypted_session_password)

			#Decrypt the randomly generated string sent from the server, to confirm the hash
			symmetric_key_confirmation = self.recv()
			confirmation_data = decrypt(session_password, symmetric_key_confirmation['data'])
			#If True, both the server and client now have an agreed upon symmetric key
			if sha256(confirmation_data) == symmetric_key_confirmation['hash']:
				self.send(confirmation_data)
				self.key = session_password

		return True
	





