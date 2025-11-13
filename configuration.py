from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QFrame, QVBoxLayout, QButtonGroup
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
    
    buttons = []
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
        buttons.append(btn)
        layout.addWidget(btn)
    
    widget.setLayout(layout)
    return widget, buttons

def create_configuration_page():
    
    page = QWidget()
    page.setStyleSheet("background-color: #000000;")
    page.setMinimumSize(1000, 540)
    layout = QGridLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)
    page.setLayout(layout)
    
    #Power Mode
    power_widget, power_buttons = create_mode_widget("Power Mode", ["Low Power Mode", "Normal Power Mode"])
    layout.addWidget(power_widget, 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    # Button group for Power Mode
    power_button_group = QButtonGroup(power_widget)
    power_button_group.setExclusive(True)
    for btn in power_buttons:
        btn.setCheckable(True)
        power_button_group.addButton(btn)
    
    # Default to Normal Power Mode
    power_buttons[1].setChecked(True)
    
    #Balance Mode
    balance_widget, balance_buttons = create_mode_widget("Balance Mode", ["Manuel Balance", "Automatic Balance"])
    layout.addWidget(balance_widget, 1, 1, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    # Button group for Balance Mode
    balance_button_group = QButtonGroup(balance_widget)
    balance_button_group.setExclusive(True)
    for btn in balance_buttons:
        btn.setCheckable(True)
        balance_button_group.addButton(btn)
    
    # Default to Automatic Balance
    balance_buttons[1].setChecked(True)
    
    def update_status_message():
        status_byte = 0
        if power_buttons[0].isChecked():  # Low Power Mode
            status_byte |= (1 << 0)
        if balance_buttons[0].isChecked():  # Manuel Balance
            status_byte |= (1 << 1)
        if operation_buttons[1].isChecked():  # Sleep BMU
            status_byte |= (1 << 3)
        if master_buttons[1].isChecked():  # BCU is Master
            status_byte |= (1 << 6)
        if request_buttons[1].isChecked():  # Push Mode
            status_byte |= (1 << 7)
        
        message_bytes = [status_byte] + [0] * 7
        message_hex = ' '.join(f"{b:02X}" for b in message_bytes)
        print(f"CAN ID 0x600: {message_hex}")
    
    def on_power_mode_changed():
        mode = "Low Power Mode" if power_buttons[0].isChecked() else "Normal Power Mode"
        print(f"Button pressed: {mode}")
        update_status_message()
    
    def on_balance_mode_changed():
        mode = "Manuel Balance" if balance_buttons[0].isChecked() else "Automatic Balance"
        print(f"Button pressed: {mode}")
        update_status_message()
    
    power_button_group.buttonClicked.connect(on_power_mode_changed)
    balance_button_group.buttonClicked.connect(on_balance_mode_changed)
    
    #Operation Mode
    operation_widget, operation_buttons = create_mode_widget("Operation Mode", ["Normal Operation", "Sleep BMU"])
    layout.addWidget(operation_widget, 1, 2, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    # Button group for Operation Mode
    operation_button_group = QButtonGroup(operation_widget)
    operation_button_group.setExclusive(True)
    for btn in operation_buttons:
        btn.setCheckable(True)
        operation_button_group.addButton(btn)
    
    # Default to Normal Operation
    operation_buttons[0].setChecked(True)
    
    def on_operation_mode_changed():
        mode = "Sleep BMU" if operation_buttons[1].isChecked() else "Normal Operation"
        print(f"Button pressed: {mode}")
        update_status_message()
    
    operation_button_group.buttonClicked.connect(on_operation_mode_changed)
    
    #RESET SYSTEM
    reset_widget, reset_buttons = create_mode_widget("RESET SYSTEM", ["RESET BMU", ""], special_case="reset")
    layout.addWidget(reset_widget, 1, 3, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    # Make Reset BMU button checkable
    reset_buttons[0].setCheckable(True)
    
    #Master Mode
    master_widget, master_buttons = create_mode_widget("Master Mode", ["BMU is Master", "BCU is Master"])
    layout.addWidget(master_widget, 2, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
    # Button group for Master Mode
    master_button_group = QButtonGroup(master_widget)
    master_button_group.setExclusive(True)
    for btn in master_buttons:
        btn.setCheckable(True)
        master_button_group.addButton(btn)
    
    # Default to BMU is Master
    master_buttons[0].setChecked(True)
    
    def on_master_mode_changed():
        mode = "BMU is Master" if master_buttons[0].isChecked() else "BCU is Master"
        print(f"Button pressed: {mode}")
        update_status_message()
    
    master_button_group.buttonClicked.connect(on_master_mode_changed)
    
    #Request Mode
    request_widget, request_buttons = create_mode_widget("Request Mode", ["Pull Mode", "Push Mode"])
    layout.addWidget(request_widget, 2, 1, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    # Button group for Request Mode
    request_button_group = QButtonGroup(request_widget)
    request_button_group.setExclusive(True)
    for btn in request_buttons:
        btn.setCheckable(True)
        request_button_group.addButton(btn)

    # Default to Pull Mode
    request_buttons[0].setChecked(True)

    def on_request_mode_changed():
        mode = "Push Mode" if request_buttons[1].isChecked() else "Pull Mode"
        print(f"Button pressed: {mode}")
        update_status_message()

    request_button_group.buttonClicked.connect(on_request_mode_changed)
    
    def on_reset_changed():
        # Send reset message
        message_bytes = [4] + [0] * 7  # 00000100 for Reset BMU
        message_hex = ' '.join(f"{b:02X}" for b in message_bytes)
        print("Button pressed: Reset BMU")
        print(f"CAN ID 0x600: {message_hex}")
        
        # Reset all other buttons to default
        power_buttons[1].setChecked(True)  # Normal Power Mode
        balance_buttons[1].setChecked(True)  # Automatic Balance
        operation_buttons[0].setChecked(True)  # Normal Operation
        master_buttons[0].setChecked(True)  # BMU is Master
        request_buttons[0].setChecked(True)  # Pull Mode
        reset_buttons[0].setChecked(False)  # Uncheck reset button
    
    reset_buttons[0].clicked.connect(on_reset_changed)
    
    return page