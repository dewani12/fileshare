import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, 
    QProgressBar, QMessageBox, QGroupBox, QGridLayout, QScrollArea, QFrame,
    QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPalette, QFont
from ui.button import AnimatedButton
from core.sender import FileSender

class SenderWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.file_path = None
        self.receivers = {} 
        self.sender_threads = {}  
        
        self.apply_dark_theme()
        
        self.init_ui()
        
    def apply_dark_theme(self):
        self.setWindowTitle("File Transfer")
        self.setMinimumSize(500, 600)
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(40, 42, 54))           
        palette.setColor(QPalette.WindowText, QColor(248, 248, 242))     
        palette.setColor(QPalette.Base, QColor(30, 31, 41))             
        palette.setColor(QPalette.AlternateBase, QColor(45, 47, 61))    
        palette.setColor(QPalette.ToolTipBase, QColor(80, 85, 105))     
        palette.setColor(QPalette.ToolTipText, QColor(248, 248, 242))   
        palette.setColor(QPalette.Text, QColor(248, 248, 242))          
        palette.setColor(QPalette.Button, QColor(60, 65, 80))           
        palette.setColor(QPalette.ButtonText, QColor(248, 248, 242))    
        palette.setColor(QPalette.BrightText, Qt.white)                 
        palette.setColor(QPalette.Link, QColor(139, 233, 253))          
        palette.setColor(QPalette.Highlight, QColor(189, 147, 249))     
        palette.setColor(QPalette.HighlightedText, Qt.black)            
        
        self.setPalette(palette)
        
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 10pt;
            }
            QGroupBox {
                border: 1px solid #6272a4;
                border-radius: 6px;
                margin-top: 12px;
                font-weight: bold;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #bd93f9;
            }
            QPushButton {
                background-color: #50fa7b;
                color: #282a36;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #85ffa3;
            }
            QPushButton:pressed {
                background-color: #41ca69;
            }
            QPushButton:disabled {
                background-color: #4f5368;
                color: #a0a0a0;
            }
            QLineEdit {
                border: 1px solid #6272a4;
                border-radius: 4px;
                padding: 6px;
                background-color: #282a36;
                color: #f8f8f2;
            }
            QProgressBar {
                border: 1px solid #6272a4;
                border-radius: 4px;
                text-align: center;
                color: #000000;
                font-weight: bold;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #50fa7b;
                border-radius: 3px;
            }
            QScrollArea {
                border: 1px solid #6272a4;
                border-radius: 4px;
            }
            QLabel {
                color: #f8f8f2;
            }
            QFrame {
                border-radius: 6px;
                background-color: #363949;
                padding: 8px;
            }
        """)
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        file_group = QGroupBox("File Selection")
        file_layout = QHBoxLayout()
        file_layout.setContentsMargins(10, 15, 10, 10)
        
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #a0a0a0; font-style: italic;")
        
        self.browse_button = AnimatedButton("Browse...")
        self.browse_button.setStyleSheet("""
            QPushButton {
                background-color: #6272a4;
                color: #f8f8f2;
            }
            QPushButton:hover {
                background-color: #7282b4;
            }
            QPushButton:pressed {
                background-color: #515c8c;
            }
        """)
        self.browse_button.clicked.connect(self.browse_file)
        
        file_layout.addWidget(self.file_label, 1)
        file_layout.addWidget(self.browse_button)
        
        file_group.setLayout(file_layout)
        
        receiver_group = QGroupBox("Receiver Configuration")
        receiver_layout = QGridLayout()
        receiver_layout.setContentsMargins(10, 15, 10, 10)
        receiver_layout.setVerticalSpacing(10)
        receiver_layout.setHorizontalSpacing(10)
        
        self.ip_label = QLabel("IP Address:")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP address...")
        
        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit("5000")
        
        self.add_receiver_button = AnimatedButton("Add Receiver")
        self.add_receiver_button.setStyleSheet("""
            QPushButton {
                background-color: #8be9fd;
                color: #282a36;
            }
            QPushButton:hover {
                background-color: #a5f1ff;
            }
            QPushButton:pressed {
                background-color: #70c1d8;
            }
        """)
        self.add_receiver_button.clicked.connect(self.add_receiver)
        
        receiver_layout.addWidget(self.ip_label, 0, 0)
        receiver_layout.addWidget(self.ip_input, 0, 1)
        receiver_layout.addWidget(self.port_label, 1, 0)
        receiver_layout.addWidget(self.port_input, 1, 1)
        receiver_layout.addWidget(self.add_receiver_button, 2, 0, 1, 2)
        
        receiver_group.setLayout(receiver_layout)
        
        receivers_group = QGroupBox("Receivers")
        receivers_layout = QVBoxLayout()
        receivers_layout.setContentsMargins(10, 15, 10, 10)
        
        self.receivers_list = QWidget()
        self.receivers_list.setStyleSheet("background-color: transparent;")
        self.receivers_layout = QVBoxLayout(self.receivers_list)
        self.receivers_layout.setSpacing(10)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.receivers_list)
        scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                background-color: #282a36;
                width: 14px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #6272a4;
                min-height: 20px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #7282b4;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: #282a36;
            }
        """)
        
        receivers_layout.addWidget(scroll_area)
        
        receivers_group.setLayout(receivers_layout)
        
        self.send_button = AnimatedButton("Send File")
        self.send_button.setMinimumHeight(50)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #ff79c6;
                color: #282a36;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff92d0;
            }
            QPushButton:pressed {
                background-color: #d64da6;
            }
            QPushButton:disabled {
                background-color: #4f5368;
                color: #a0a0a0;
            }
        """)
        self.send_button.clicked.connect(self.send_file)
        self.send_button.setEnabled(False)
        
        layout.addWidget(file_group)
        layout.addWidget(receiver_group)
        layout.addWidget(receivers_group, 1)  
        layout.addWidget(self.send_button)
        
        self.setLayout(layout)
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        
        if file_path:
            self.file_path = file_path
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            size_str = self.format_size(file_size)
            
            self.file_label.setText(f"{file_name} ({size_str})")
            self.file_label.setStyleSheet("color: #50fa7b; font-weight: bold;")
            self.update_send_button()
    
    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    def add_receiver(self):
        ip = self.ip_input.text().strip()
        port = self.port_input.text().strip()
        
        if not ip:
            QMessageBox.warning(self, "Invalid IP", "Please enter a valid IP address.")
            return
            
        if not port or not port.isdigit():
            QMessageBox.warning(self, "Invalid Port", "Please enter a valid port number.")
            return
            
        port = int(port)
        
        if ip in self.receivers:
            QMessageBox.warning(self, "Duplicate IP", f"Receiver {ip} is already added.")
            return
        
        receiver_frame = QFrame()
        receiver_frame.setFrameShape(QFrame.StyledPanel)
        receiver_frame.setFrameShadow(QFrame.Raised)
        receiver_frame.setStyleSheet("""
            QFrame {
                background-color: #44475a;
                border: 1px solid #6272a4;
                padding: 10px;
                margin: 2px;
            }
        """)
        
        receiver_layout = QGridLayout(receiver_frame)
        receiver_layout.setContentsMargins(10, 10, 10, 10)
        receiver_layout.setSpacing(8)
        
        ip_label = QLabel(f"IP: {ip} | Port: {port}")
        ip_label.setStyleSheet("font-weight: bold; color: #8be9fd;")
        
        status_label = QLabel("Status: Ready")
        status_label.setStyleSheet("color: #f1fa8c;")
        
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setTextVisible(True)
        progress_bar.setFormat("%p%")
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #6272a4;
                border-radius: 4px;
                text-align: center;
                color: #000000;
                font-weight: bold;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #50fa7b;
                border-radius: 3px;
            }
        """)
        
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                color: #f8f8f2;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff6e6e;
            }
            QPushButton:pressed {
                background-color: #e64747;
            }
        """)
        remove_button.clicked.connect(lambda: self.remove_receiver(ip))
        
        receiver_layout.addWidget(ip_label, 0, 0)
        receiver_layout.addWidget(status_label, 0, 1)
        receiver_layout.addWidget(remove_button, 0, 2)
        receiver_layout.addWidget(progress_bar, 1, 0, 1, 3)
        
        self.receivers_layout.addWidget(receiver_frame)
        
        animate_timer = QTimer()
        animate_timer.timeout.connect(lambda: self.animate_progress_bar(progress_bar))
        
        self.receivers[ip] = (status_label, progress_bar, animate_timer, receiver_frame, port)
        
        self.ip_input.clear()
        self.port_input.setText("5000")  
        
        self.update_send_button()
    
    def remove_receiver(self, ip):
        if ip in self.receivers:
            _, _, timer, frame, _ = self.receivers[ip]
            timer.stop()
            
            if ip in self.sender_threads:
                thread = self.sender_threads[ip]
                if thread.isRunning():
                    thread.terminate()
                    thread.wait()  
                del self.sender_threads[ip]
            
            self.receivers_layout.removeWidget(frame)
            frame.deleteLater()
            
            del self.receivers[ip]
            
            self.update_send_button()
    
    def update_send_button(self):
        self.send_button.setEnabled(bool(self.file_path and self.receivers))
    
    def animate_progress_bar(self, progress_bar):
        value = progress_bar.value()
        
        if value < 30:
            color = "#ff5555"  
        elif value < 70:
            color = "#f1fa8c"  
        else:
            color = "#50fa7b"  
            
        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #6272a4;
                border-radius: 4px;
                text-align: center;
                color: #000000;
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
    
    def send_file(self):
        if not self.file_path:
            QMessageBox.warning(self, "No File Selected", "Please select a file to send.")
            return
        
        if not self.receivers:
            QMessageBox.warning(self, "No Receivers", "Please add at least one receiver.")
            return
        
        for ip, (status_label, progress_bar, timer, _, port) in self.receivers.items():
            status_label.setText("Status: Connecting...")
            status_label.setStyleSheet("color: #8be9fd;")
            
            timer.start(100)
            
            sender = FileSender(ip, port, self.file_path)
            sender.status_update.connect(self.update_receiver_status)
            sender.progress_update.connect(self.update_receiver_progress)
            sender.transfer_complete.connect(self.handle_transfer_complete)
            sender.start()
            
            self.sender_threads[ip] = sender
    
    def update_receiver_status(self, ip, message):
        if ip in self.receivers:
            status_label, _, _, _, _ = self.receivers[ip]
            status_label.setText(f"Status: {message}")
    
    def update_receiver_progress(self, ip, value):
        if ip in self.receivers:
            _, progress_bar, _, _, _ = self.receivers[ip]
            progress_bar.setValue(value)
    
    def handle_transfer_complete(self, ip, success):
        if ip in self.receivers:
            status_label, progress_bar, timer, _, _ = self.receivers[ip]
            
            timer.stop()
            
            if success:
                status_label.setText("Status: Complete")
                status_label.setStyleSheet("font-weight: bold; color: #50fa7b;")
            else:
                status_label.setText("Status: Failed")
                status_label.setStyleSheet("font-weight: bold; color: #ff5555;")
            
            if ip in self.sender_threads:  
                thread = self.sender_threads[ip]
                if thread.isRunning():
                    thread.quit()
                    thread.wait(1000) 
                del self.sender_threads[ip]
    
    def closeEvent(self, event):
        """Handle application closing properly by terminating all threads"""
        for ip, (_, _, timer, _, _) in self.receivers.items():
            timer.stop()
        
        for ip, thread in list(self.sender_threads.items()):
            if thread.isRunning():
                thread.terminate()
                thread.wait(1000)  
            del self.sender_threads[ip]
        
        event.accept()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    window = SenderWidget()
    window.show()
    
    sys.exit(app.exec_())