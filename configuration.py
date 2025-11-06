from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

def create_configuration_page():
    
    page = QWidget()
    page.setStyleSheet("background-color: #000000;")
    page.setMinimumSize(1000, 540)
    layout = QGridLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)
    page.setLayout(layout)
    return page