import os
import socket
from PyQt5.QtCore import QThread, pyqtSignal

class FileSender(QThread):
    progress_update = pyqtSignal(str, int)
    status_update = pyqtSignal(str, str)
    transfer_complete = pyqtSignal(str, bool)
    
    def __init__(self, ip, port, file_path):
        super().__init__()
        self.ip = ip
        self.port = port
        self.file_path = file_path
        
    def run(self):
        self.status_update.emit(self.ip, "Connecting...")
        
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(10)  
            client_socket.connect((self.ip, self.port))
            
            file_name = os.path.basename(self.file_path)
            file_size = os.path.getsize(self.file_path)
            
            file_info = f"{file_name}|{file_size}"
            client_socket.send(file_info.encode())
            
            response = client_socket.recv(1024).decode()
            if response != "READY":
                self.status_update.emit(self.ip, "Error: Receiver not ready")
                client_socket.close()
                self.transfer_complete.emit(self.ip, False)
                return
            
            self.status_update.emit(self.ip, f"Sending {file_name}")
            
            with open(self.file_path, 'rb') as f:
                bytes_sent = 0
                buffer_size = 4096
                
                while True:
                    buffer = f.read(buffer_size)
                    if not buffer:
                        break
                    
                    client_socket.send(buffer)
                    bytes_sent += len(buffer)
                    progress = int((bytes_sent / file_size) * 100)
                    self.progress_update.emit(self.ip, progress)
                    
            client_socket.close()
            self.status_update.emit(self.ip, "Transfer complete!")
            self.transfer_complete.emit(self.ip, True)
            
        except Exception as e:
            self.status_update.emit(self.ip, f"Error: {str(e)}")
            self.transfer_complete.emit(self.ip, False)