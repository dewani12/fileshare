from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)
        
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(100)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        rect = self.geometry()
        target_rect = QRect(rect.x() - 2, rect.y() - 2, rect.width() + 4, rect.height() + 4)
        self._animation.setStartValue(rect)
        self._animation.setEndValue(target_rect)
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        rect = self.geometry()
        target_rect = QRect(rect.x() + 2, rect.y() + 2, rect.width() - 4, rect.height() - 4)
        self._animation.setStartValue(rect)
        self._animation.setEndValue(target_rect)
        self._animation.start()
        super().leaveEvent(event)