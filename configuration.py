from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt

def create_mode_widget(title, button_texts, special_case=None):  # hepis aynı diye tek fonksiyon oluşturup hepsini burada topladım.
    widget = QFrame()
    widget.setStyleSheet('''
        QFrame {
            background-color: transparent;
            border: 4px solid #0077A8;
            border-radius: 10px;
        }
    ''')
    widget.setFixedSize(200, 140)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)
    
    title_label = QLabel(title)
    title_label.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: bold; background: transparent; border: none;")
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title_label)
    
    for i, text in enumerate(button_texts):  # butonlar ile alakalı fonksiyon.
        btn = QPushButton(text)
        if special_case == "reset" and i == 1:
            btn.setText("")
            btn.setEnabled(False)
            btn.setStyleSheet('''
                QPushButton {
                    background-color: transparent;
                    color: #ffffff;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: rgba(0,119,168,0.1);
                }
                QPushButton:pressed {
                    background-color: #0077A8;
                    color: #000000;
                }
            ''')
        else:
            btn.setStyleSheet('''
                QPushButton {
                    background-color: transparent;
                    color: #ffffff;
                    border: 2px solid #0077A8;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: rgba(0,119,168,0.1);
                }
                QPushButton:pressed {
                    background-color: #0077A8;
                    color: #000000;
                }
            ''')
        btn.setFixedHeight(40)
        
        layout.addWidget(btn)
    
    widget.setLayout(layout)
    return widget

def create_configuration_page():
    
    page = QWidget()
    page.setStyleSheet("background-color: #000000;")
    page.setMinimumSize(1000, 540)
    layout = QGridLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)
    page.setLayout(layout)
    
    #Power Mode
    power_widget = create_mode_widget("Power Mode", ["Low Power Mode", "Normal Power Mode"])
    layout.addWidget(power_widget, 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    #Balance Mode
    balance_widget = create_mode_widget("Balance Mode", ["Manuel Balance", "Automatic Balance"])
    layout.addWidget(balance_widget, 1, 1, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    #Operation Mode
    operation_widget = create_mode_widget("Operation Mode", ["Normal Operation", "Sleep BMU"])
    layout.addWidget(operation_widget, 1, 2, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    #RESET SYSTEM
    reset_widget = create_mode_widget("RESET SYSTEM", ["RESET BMU", ""], special_case="reset")
    layout.addWidget(reset_widget, 1, 3, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    #Master Mode
    master_widget = create_mode_widget("Master Mode", ["BMU is Master", "BCU is Master"])
    layout.addWidget(master_widget, 2, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    #Request Mode
    request_widget = create_mode_widget("Request Mode", ["Pull Mode", "Push Mode"])
    layout.addWidget(request_widget, 2, 1, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    return page