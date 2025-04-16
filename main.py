import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QTabWidget,QWidget,QVBoxLayout
from ui.sender_widget import SenderWidget
from ui.reciever_widget import ReceiverWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P2P File Transfer")
        self.setMinimumSize(600,500)

        central_widget=QWidget()
        self.setCentralWidget(central_widget)
        main_layout=QVBoxLayout(central_widget)

        tab_widget=QTabWidget()
        self.sender_widget=SenderWidget()
        self.receiver_widget=ReceiverWidget()

        tab_widget.addTab(self.sender_widget,"Send Files")
        tab_widget.addTab(self.receiver_widget,"Receive Files")

        main_layout.addWidget(tab_widget)
        self.set_style()

    def set_style(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #000000;
            color: #e0e0e0;
        }
        QWidget {
            background-color: #000000;
            color: #d0d0d0;
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }
        QTabWidget::pane {
            border: 1px solid #1a1a1a;
            border-radius: 6px;
            background-color: #0d0d0d;
        }
        QTabBar::tab {
            background-color: #1a1a1a;
            color: #f0f0f0;
            border: 1px solid #2a2a2a;
            border-bottom: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding: 8px 14px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #3a3a3a;
            color: #ffffff;
            border: 1px solid #3a3a3a;
            border-bottom: 1px solid #0d0d0d;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #2a2a2a;
            border-radius: 6px;
            margin-top: 15px;
            padding: 10px;
            background-color: #0d0d0d;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 6px;
        }
        QLineEdit,QListWidget,QProgressBar {
            background-color: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 4px;
            padding: 6px;
            color: #ffffff;
        }
        QLineEdit:focus,QListWidget:focus {
            border: 1px solid #6a6a6a;
        }
        QProgressBar {
            text-align: center;
            background-color: #1a1a1a;
            color: #ffffff;
        }
        QProgressBar::chunk {
            background-color: #5e5e5e;
            border-radius: 3px;
        }
        QPushButton {
            background-color: #444444;
            color: #ffffff;
            border-radius: 5px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #555555;
        }
        QPushButton:pressed {
            background-color: #666666;
        }
    """)


def main():
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
