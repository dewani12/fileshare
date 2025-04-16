import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QGroupBox,
    QProgressBar, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from ui.button import AnimatedButton
from core.reciever import FileReceiver

class ReceiverWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        self.start_server()
        
    def init_ui(self):

        layout = QVBoxLayout()

        server_group = QGroupBox("Receiver Settings")
        server_layout = QGridLayout()
        
        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit("5000")
        
        self.server_status = QLabel("Server: Stopped")
        self.server_status.setStyleSheet("font-weight: bold;")
        
        self.start_button = AnimatedButton("Start Server")
        self.start_button.clicked.connect(self.start_server)
        
        self.stop_button = AnimatedButton("Stop Server")
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)
        
        server_layout.addWidget(self.port_label, 0, 0)
        server_layout.addWidget(self.port_input, 0, 1)
        server_layout.addWidget(self.server_status, 1, 0, 1, 2)
        server_layout.addWidget(self.start_button, 2, 0)
        server_layout.addWidget(self.stop_button, 2, 1)
        
        server_group.setLayout(server_layout)
        
        transfer_group = QGroupBox("Transfer Status")
        transfer_layout = QVBoxLayout()
        
        self.status_list = QListWidget()
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        transfer_layout.addWidget(self.status_list)
        transfer_layout.addWidget(self.progress_bar)
        
        transfer_group.setLayout(transfer_layout)
        
        layout.addWidget(server_group)
        layout.addWidget(transfer_group)
        
        self.setLayout(layout)
        
    def start_server(self):
        try:
            port = int(self.port_input.text())
            
            self.receiver = FileReceiver(port=port)
            self.receiver.status_update.connect(self.update_status)
            self.receiver.progress_update.connect(self.update_progress)
            self.receiver.transfer_complete.connect(self.handle_transfer_complete)
            self.receiver.start()
            
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.port_input.setEnabled(False)
            self.server_status.setText("Server: Running")
            self.server_status.setStyleSheet("font-weight: bold; color: green;")
            
        except ValueError:
            QMessageBox.warning(self, "Invalid Port", "Please enter a valid port number.")
    
    def stop_server(self):
        if hasattr(self, 'receiver'):
            self.receiver.stop()
            
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.port_input.setEnabled(True)
        self.server_status.setText("Server: Stopped")
        self.server_status.setStyleSheet("font-weight: bold; color: red;")
    
    def update_status(self, message):
        self.status_list.addItem(f"{time.strftime('%H:%M:%S')} - {message}")
        self.status_list.scrollToBottom()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        
        if value > 0:
            r = int(255 * (100 - value) / 100)
            g = int(255 * value / 100)
            b = 0
            self.progress_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: rgb({r}, {g}, {b}); }}")
    
    def handle_transfer_complete(self, file_path):
        QMessageBox.information(self, "Transfer Complete", f"File saved to:\n{file_path}")