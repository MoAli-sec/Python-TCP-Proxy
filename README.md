# Python-TCP-Proxy

<<<<<<< HEAD
This Python script is a simple implementation of a proxy server that intercepts and inspects requests and responses. It was inspired by the book "Black Hat Python" by Justin Seitz. 
The script allows users to modify both incoming requests and outgoing responses, and can be used for educational or testing purposes. 
The script uses the socket module to handle network communication, threading to manage multiple client connections.
=======
This Python script is a simple implementation of a proxy server that intercepts and inspects requests and responses. It was inspired by the book "Black Hat Python" by Justin Seitz. <br />The script allows users to modify both incoming requests and outgoing responses, and can be used for educational or testing purposes. <br />The script uses the socket module to handle network communication, threading to manage multiple client connections.
>>>>>>> bd5a796 (first initial)

# Requirements
- python3
- socket, sys, threading modules

# Usage
The script can be run using the following command:

`
pyhton proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]
`

# Examples
```
python proxy.py 127.0.0.1 9000 [remoteserver_ip] 9000 True
python proxy.py 192.168.1.203 21 [ftp_servername] 21 True
```

# Modifying requests and responses
This script allows you to modify both incoming requests and outgoing responses. <br />
and i added three examples you can use in the `request_handler()` and `response_handler()` functions. <br />
1: Modifying the Contents. These modifications can help simulate different scenarios or test how the system handles altered data. <br />
2: Performing Fuzzing Tasks. Additional data is injected to test the system's robustness against unexpected inputs. <br />
3: Testing for Authentication Issues. This can be used to test how the system handles different authentication scenarios, such as weak passwords or incorrect credentials

# Disclaimer
This tool is intended for educational and testing purposes only. Please use responsibly and with the explicit permission of the remote server owner.
