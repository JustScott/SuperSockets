# <p align='center'>SuperSockets</p>
<h3 align='center'> Easy to use implementation of python3's built in 'socket' library </h3>

<br>
<br>

# Example Use

<h4>Server Configuration</h4>

```python
#Create connection
server = connect(ip="0.0.0.0", port="1001", connection_type="server", RSA=True)

server.send("Can you here me?")
print(server.recv())
```
<h4>Client Configuration</h4>

```python
from supersockets import connect

#Connect to server
client = connect(ip="0.0.0.0", port="1001", connection_type="client", RSA=True)

print(server.recv())
client.send("Loud and clear!")
```

<br>

<h2>Required Dependences From PyPi</h2>

<h4>pycryptodome == 3.15.0</h4>

- <a href="https://github.com/Legrandin/pycryptodome">pycryptodome on GitHub</a>

- <a href="https://pypi.org/project/pycryptodome/">pycryptodome on PyPi</a>

<h4>listcrypt == 0.2.2</h4>

- <a href="https://github.com/JustScott/ListCrypt">listcrypt on GitHub</a>

- <a href="https://pypi.org/project/listcrypt/">listcrypt on PyPi</a>

<h4>rapidrsa == 0.0.6</h4>

- <a href="https://github.com/JustScott/RapidRSA">rapidrsa on GitHub</a>

- <a href="https://pypi.org/project/rapidrsa/">rapidrsa on PyPi</a>

<br>


# Documentation
```python
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
```
