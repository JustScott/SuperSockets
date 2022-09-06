# <p align='center'>SuperSockets</p>
<h3 align='center'> Easy to use implementation of python3's built in 'socket' library </h3>

<br>
<br>

# Example Use

<h4>Server Configuration</h4>

```python
''' file: example_server.py '''

from supersockets import server

#Create connection
s = server(ip="0.0.0.0", port=11000, RSA=True)

s.send("Can you here me?")
print(s.recv())


''' Output '''
~$ python3 example_server.py
Loud and clear!

```
<h4>Client Configuration</h4>

```python
'''file: example_client.py '''

from supersockets import client

#Connect to server
c = client(ip="0.0.0.0", port=11000)

print(c.recv())
c.send("Loud and clear!")


''' Output '''
~$ python3 example_client.py
Can you here me?

```

<br>

<h2>Required Dependences From PyPi</h2>

<h4>pycryptodome >= 3.15.0</h4>

- <a href="https://github.com/Legrandin/pycryptodome">pycryptodome on GitHub</a>

- <a href="https://pypi.org/project/pycryptodome/">pycryptodome on PyPi</a>

<h4>listcrypt >= 1.0.0</h4>

- <a href="https://github.com/JustScott/ListCrypt">listcrypt on GitHub</a>

- <a href="https://pypi.org/project/listcrypt/">listcrypt on PyPi</a>

<h4>rapidrsa >= 1.0.0</h4>

- <a href="https://github.com/JustScott/RapidRSA">rapidrsa on GitHub</a>

- <a href="https://pypi.org/project/rapidrsa/">rapidrsa on PyPi</a>

<br>


# Documentation
```python
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
```
