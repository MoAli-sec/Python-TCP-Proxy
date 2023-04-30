# importing libraries
import sys
import socket
import threading

# HEX_FILTER is a translation table string used to filter non-printable characters in the hexdump function
# It maps each character in the range of 0 to 255 to '.' if it is non-printable, or the character itself if it is printable
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hexdump(src, length=16, show=True):
    """
    Prints the input as hexadecimal format to the console

    Args:
        src (bytes or str): The input to be hexdumped. If bytes, it will be decoded as a string.
        length (int): The number of bytes per line in the hexdump output. Defaults to 16.
        show (bool): Determines whether to print the hexdump output to the console or return it as a list. Defaults to True.

    Returns:
        list: List of lines in the hexdump output, if show is set to False.
    """

    # If the input is of type bytes, decode it as a string
    if isinstance(src, bytes):
        src = src.decode()

    results = []  # List to store each line of the hexdump output
    for i in range(0, len(src), length):
        word = str(src[i:i+length])  # Get a slice of the input string of length 'length'

        # Translate each character in the slice using the HEX_FILTER translate table
        printable = word.translate(HEX_FILTER)

        # Convert each character to its corresponding hexadecimal representation
        hexa = " ".join([f'{ord(c):02x}' for c in word])

        hexwidth = length*3  # Calculate the width of the hexadecimal representation
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')  # Create a formatted string for each line of output
    if show:
        # If 'show' is True, print each line of the hexdump output
        for line in results:
            print(line)
    else:
        # If 'show' is False, return the list of lines in the hexdump output
        return results


def receive_from(connection):
    """
    Receives data from a connection until there is no more data available or a timeout occurs.

    Args:
        connection (socket.socket): The connection to receive data from.

    Returns:
        bytes: The received data.
    """
    buffer = b""  # Buffer to store the received data
    connection.settimeout(5)  # Set a timeout of 5 seconds for the connection
    try:
        while True:
            data = connection.recv(4096)  # Receive data in chunks of 4096 bytes
            if not data:
                break  # Break the loop if no more data is received
            buffer += data  # Append the received data to the buffer
    except Exception:
        pass
    return buffer  # Return the received data


"""
The coming two functions are because we may want to modify the response or request
packets before the proxy send them on their way
"""
def request_handler(buffer):
    # 1: Modifying the Contents.
    """
    Modifies the request packet by replacing occurrences of "admin" with "attacker".

    Args:
        buffer (bytes): The original request packet.

    Returns:
        bytes: The modified request packet.
    """
    # These modifications can help simulate different scenarios or test how the system handles altered data.
    # Modify the packet content by replacing "admin" with "attacker"
    # modified_buffer = buffer.replace(b'Hello', b'Modified Hello')
    # return modified_buffer

    # 2: Performing Fuzzing Tasks.
    """
    Modifies the request packet by adding 'A' byte multiplied by 100 at the beginning.

    Args:
        buffer (bytes): The original request packet.

    Returns:
        bytes: The modified request packet.
    """
    # This is a simple example of payload fuzzing, where additional data is injected to test the system's robustness against unexpected inputs.
    # Perform fuzzing tasks by adding 'A' byte multiplied by 100 at the beginning
    # modified_buffer = buffer + b"A" * 100
    # return modified_buffer

    # 3: Testing for Authentication Issues
    """
    Test for authentication errors by replacing "password=123456" with "password=weakpassword" if it exists in the request packet.

    Args:
        buffer (bytes): The original request packet.

    Returns:
        bytes: The modified request packet, with "password=123456" replaced with "password=weakpassword" if it exists.
    """
    # This can be used to test how the system handles different authentication scenarios, such as weak passwords or incorrect credentials
    # Test for authentication errors by replacing "password=123456" with "password=weakpass"
    # if b"password=123456" in modified_buffer:
    #     print("Potential authentication error detected!")
    #     modified_buffer = modified_buffer.replace(b"password=123456", b"password=weakpass")
    # return modified_buffer
    return buffer


def response_handler(buffer):
    # 1
    """
    Modifies the response packet by replacing occurrences of "welcome" with "unauthorized".

    Args:
        buffer (bytes): The original response packet.

    Returns:
        bytes: The modified response packet.
    """
    # Modify the packet content by replacing "welcome" with "unauthorized"
    # modified_buffer = buffer.replace(b'welcome', b'unauthorized')
    # return modified_buffer

    # 2
    # Do not modify the response packet
    # return buffer

    # 3
    """
    Tests for authentication errors by checking for the "authentication failed" message.

    Args:
        buffer (bytes): The original response packet.

    Returns:
        bytes: The modified response packet.
    """
    # If the "authentication failed" message is detected in the response, print a warning message and return the original buffer.
    # if b"authentication failed" in buffer.lower():
    #     print("Authentication failed detected!")
    # return buffer
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    """
    This function handles the proxy communication between the client and remote host.
    :param client_socket: The socket object representing the client connection.
    :param remote_host: The hostname of the remote host to connect to.
    :param remote_port: The port number of the remote host to connect to.
    :param receive_first: Boolean indicating whether to receive data from the remote host first.
    """
    # Create a new socket object to connect to the remote host and port
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # If receive_first is true, receive data from the remote socket and display it
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    # Handle the response received from the remote host
    remote_buffer = response_handler(remote_buffer)
    # If the response buffer is not empty, send it to the client socket
    if len(remote_buffer):
        print("[<==] Sending %d bytes from localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)

    # Continuously receive data from the client socket and send it to the remote host
    # Then, receive data from the remote host and send it back to the client socket
    while True:
        # Receive data from the client socket and display it
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>] Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)

            # Handle the request received from the client socket
            local_buffer = request_handler(local_buffer)
            # Send the request to the remote host
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        # Receive data from the remote host and display it
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            # Handle the response received from the remote host
            remote_buffer = response_handler(remote_buffer)
            # Send the response back to the client socket
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        # If there is no more data to receive from either the client socket or the remote host,
        # close both sockets and break out of the loop
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


def server_loop(local_host, local_port,
                remote_host, remote_port, receive_first):
    """
    This function sets up a listening socket on a specified local host and port, then waits for incoming client
    connections. For each incoming client connection, the function creates a new thread to handle the communication
    between the client and a remote host. The remote host is specified by a hostname and port number. The function
    can also optionally receive data from the remote host first.

    :param local_host: The hostname of the local interface to listen on.
    :param local_port: The port number of the local interface to listen on.
    :param remote_host: The hostname of the remote host to connect to.
    :param remote_port: The port number of the remote host to connect to.
    :param receive_first: Boolean indicating whether to receive data from the remote host first.
    """
    # Create a new socket object using the IPv4 address family and TCP protocol
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the specified local host and port
        server.bind((local_host, local_port))
    except Exception as e:
        # If there's an exception when binding, print an error message and exit the program
        print("Problem on bind: %r" % e)

        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    # Print a message indicating that the server is listening on the specified local host and port
    print("[*] Listening on %s:%d" % (local_host, local_port))

    # Start listening for incoming connections
    server.listen(5)

    # Loop forever, accepting incoming client connections and starting a new thread to handle each one
    while True:
        # Accept a new client connection and retrieve the client socket object and client address
        client_socket, addr = server.accept()

        # Print out information about the incoming connection
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)

        # Start a new thread to handle the incoming connection
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def main():
    """
    This function is the entry point of the program. It parses the command line arguments, extracts the relevant
    information and starts the proxy server loop.
    """
    # Check if the command line arguments are valid
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end=" ")
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    # Extract the relevant information from the command line arguments to use them in the server loop function
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5]

    # Convert the receive_first argument to a boolean value
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # Start the proxy server loop
    server_loop(local_host, local_port,
                remote_host, remote_port, receive_first)

# If this script is run directly, execute the main function
if __name__ == "__main__":
    main()


