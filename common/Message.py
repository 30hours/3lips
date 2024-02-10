"""
@file Message.py
@author 30hours
"""

import socket
import threading
import asyncio

class Message:

    """
    @class Message
    @brief A class for simple TCP messaging using a listener and sender.
    """

    def __init__(self, host, port):

        """
        @brief Constructor for Message.
        @param host (str): The host to bind the listener to.
        @param port (int): The port to bind the listener to.
        """
      
        self.host = host
        self.port = port
        self.server_socket = None
        self.callback_message_received = None

    def start_listener(self):

        """
        @brief Start the TCP listener to accept incoming connections.
        @details Ensure this function is run in a separate thread.
        @return None.
        """

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print(f"Listener is waiting for connections on {self.host}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

    def handle_client(self, conn, addr):

        """
        @brief Handle communication with a connected client.
        @param conn (socket.socket): The socket object for the connected client.
        @param addr (tuple): The address (host, port) of the connected client.
        @return None.
        """

        with conn:

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                decoded_data = data.decode()

                # Call the callback function if set
                if self.callback_message_received:
                    reply = asyncio.run(self.callback_message_received(decoded_data))
                    if reply:
                      conn.sendall(reply.encode())

    def send_message(self, message):

        """
        @brief Send a message to the specified host and port.
        @param message (str): The message to be sent.
        @return None.
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(3)
            try:
                client_socket.connect((self.host, self.port))
                client_socket.sendall(message.encode())
                reply = client_socket.recv(1024).decode()
                return reply
            except ConnectionRefusedError:
                print(f"Connection to {self.host}:{self.port} refused.")

    def set_callback_message_received(self, callback):

        """
        @brief Set callback function when a message is received.
        @param callback (function): The callback function.
        @return None.
        """

        self.callback_message_received = callback

    def close_listener(self):

        """
        @brief Close the listener socket.
        @return None.
        """

        if self.server_socket:
            self.server_socket.close()