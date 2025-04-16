import os
import socket
from PyQt5.QtCore import QThread, pyqtSignal

class FileReceiver(QThread):
    progress_update = pyqtSignal(int)
    status_update = pyqtSignal(str)
    transfer_complete = pyqtSignal(str)
    
    def __init__(self, port=5000, save_dir="Downloads"):
        super().__init__()
        self.port = port
        self.save_dir = save_dir
        self.running = True
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def run(self):
        self.status_update.emit("Starting receiver server...")
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind(('0.0.0.0', self.port))
            server_socket.listen(5)
            
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            self.status_update.emit(f"Server running on {local_ip}:{self.port}")
            
            while self.running:
                self.status_update.emit("Waiting for connections...")
                server_socket.settimeout(1)
                
                try:
                    client_socket, addr = server_socket.accept()
                    self.status_update.emit(f"Connection from {addr[0]}")
                    
                    file_info = client_socket.recv(1024).decode()
                    file_name, file_size = file_info.split('|')
                    file_size = int(file_size)
                    
                    self.status_update.emit(f"Receiving {file_name} ({file_size} bytes)")
                    
                    file_path = os.path.join(self.save_dir, file_name)
                    
                    client_socket.send("READY".encode())
                    
                    with open(file_path, 'wb') as f:
                        bytes_received = 0
                        while bytes_received < file_size:
                            buffer = client_socket.recv(4096)
                            if not buffer:
                                break
                            f.write(buffer)
                            bytes_received += len(buffer)
                            progress = int((bytes_received / file_size) * 100)
                            self.progress_update.emit(progress)
                    
                    client_socket.close()
                    self.status_update.emit(f"File saved to {file_path}")
                    self.transfer_complete.emit(file_path)
                    self.progress_update.emit(0)  
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    self.status_update.emit(f"Error: {str(e)}")
        
        except Exception as e:
            self.status_update.emit(f"Server error: {str(e)}")
        finally:
            server_socket.close()
            self.status_update.emit("Server stopped")
    
    def stop(self):
        self.running = False
        self.wait()