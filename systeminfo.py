from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QDialog, QPushButton, QButtonGroup
from PyQt6.QtCore import Qt

system_info_page = None
wake_up_button = None
sleep_button = None
info_labels = []  # List to hold value labels for updating


class ConfirmationDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmation")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #000000;
                color: #ffffff;
                border: 4px solid #0077A8;
                border-radius: 10px;
            }
        """)
        self.setModal(True)
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        label = QLabel(message)
        label.setStyleSheet("color: #ffffff; font-size: 14px; background: transparent;")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        yes_button = QPushButton("Yes")
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: #0077A8;
                color: #000000;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005577;
            }
        """)
        yes_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ffffff;
                border: 2px solid #0077A8;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 119, 168, 0.1);
            }
        """)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        self.setLayout(layout)


def create_system_info_page():
    global system_info_page, wake_up_button, sleep_button
    
    system_info_page = QWidget()
    system_info_page.setStyleSheet("background-color: #000000;")
    system_info_page.setMinimumSize(1000, 540)
    
    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)
    
    # Accent color
    accent_color = "#0077A8"
    
    # Button styles
    normal_style = f"""
    QPushButton {{
        background-color: transparent;
        color: #ffffff;
        border: 3px solid {accent_color};
        border-radius: 10px;
        font-weight: bold;
        font-size: 16px;
    }}
    QPushButton:hover {{
        background-color: rgba(0,119,168,0.1);
    }}
    """
    
    selected_style = f"""
    QPushButton {{
        background-color: {accent_color};
        color: #000000;
        border: 3px solid {accent_color};
        border-radius: 10px;
        font-weight: bold;
        font-size: 16px;
    }}
    """
    
    # Create button container frame
    button_container = QFrame()
    button_container.setStyleSheet("background-color: transparent; border: none;")
    button_container.setFixedSize(300, 100)
    
    button_layout = QHBoxLayout()
    button_layout.setContentsMargins(0, 0, 0, 0)
    button_layout.setSpacing(15)
    
    # Wake Up button
    wake_up_button = QPushButton("Wake Up")
    wake_up_button.setCheckable(True)
    wake_up_button.setFixedSize(140, 100)
    wake_up_button.setCursor(Qt.CursorShape.PointingHandCursor)
    
    # Sleep button
    sleep_button = QPushButton("Sleep")
    sleep_button.setCheckable(True)
    sleep_button.setFixedSize(140, 100)
    sleep_button.setCursor(Qt.CursorShape.PointingHandCursor)
    
    # Button group for exclusive selection
    button_group = QButtonGroup(button_container)
    button_group.setExclusive(True)
    button_group.addButton(wake_up_button)
    button_group.addButton(sleep_button)
    
    # Default to none selected (both off)
    wake_up_button.setChecked(False)
    sleep_button.setChecked(False)
    
    def update_button_styles():
        wake_up_button.setStyleSheet(selected_style if wake_up_button.isChecked() else normal_style)
        sleep_button.setStyleSheet(selected_style if sleep_button.isChecked() else normal_style)
    
    def on_wake_up_toggled(checked):    
        # bu fonksiyonda alt kısımda print ksımında wake up var bu butona tıklandıktan sonra girlecek tüm can komutları özel fonksyon ve şartları bu foknksiyon altına yazman gerekiyoe.

        if checked:
            # Kapalıdan açığa geçiş - popup onaylanmadan butonu geri al
            wake_up_button.blockSignals(True)
            wake_up_button.setChecked(False)
            wake_up_button.blockSignals(False)
            
            # Popup göster
            dialog = ConfirmationDialog("Wake Up will be activated, are you sure?", parent=system_info_page)
            if dialog.exec() == QDialog.DialogCode.Accepted:

                sleep_button.blockSignals(True)
                sleep_button.setChecked(False)
                sleep_button.blockSignals(False)
                
                wake_up_button.blockSignals(True)
                wake_up_button.setChecked(True)
                wake_up_button.blockSignals(False)
                
                print("Wake Up")   

                update_button_styles()
            else:
                update_button_styles()
        else:
            update_button_styles()
    
    def on_sleep_toggled(checked):
        # bu fonksiyonda alt kısımda print ksımında sleep  var bu butona tıklandıktan sonra girlecek tüm can komutları özel fonksyon ve şartları bu foknksiyon altına yazman gerekiyoe.


        if checked:
            
            sleep_button.blockSignals(True)
            sleep_button.setChecked(False)
            sleep_button.blockSignals(False)            
            dialog = ConfirmationDialog("Sleep will be activated, are you sure?", parent=system_info_page)

            if dialog.exec() == QDialog.DialogCode.Accepted:

                wake_up_button.blockSignals(True)
                wake_up_button.setChecked(False)
                wake_up_button.blockSignals(False)

                sleep_button.blockSignals(True)
                sleep_button.setChecked(True)
                sleep_button.blockSignals(False)
                
                print("Sleep")
                update_button_styles()
            else:
                update_button_styles()
        else:
            update_button_styles()
    
    wake_up_button.toggled.connect(on_wake_up_toggled)
    sleep_button.toggled.connect(on_sleep_toggled)
    
    update_button_styles()
    
    button_layout.addWidget(wake_up_button)
    button_layout.addWidget(sleep_button)
    button_container.setLayout(button_layout)
    
    main_layout.addWidget(button_container, 0, Qt.AlignmentFlag.AlignTop)
    
    right_container = QFrame()
    right_container.setStyleSheet('''
        QFrame {
            background-color: transparent;
            border: 3px solid #0077A8;
            border-radius: 10px;
        }
    ''')

    right_container.setMinimumHeight(500)     
    right_layout = QVBoxLayout()
    right_layout.setContentsMargins(20, 20, 20, 20)
    right_layout.setSpacing(0)    
    accent_color = "#0077A8"
    
    info_items = [
        ("🔌", "Pre-Charge Contactor:", "OFF"),
        ("🔌", "Charge Contactor:", "OFF"),
        ("🔌", "Discharge Contactor:", "OFF"),
        ("🔌", "AUX Contactor:", "OFF"),
        ("⚡", "Battery Max Current:", "0.00 A")
    ]
    
    global info_labels   # bu değerleri ileride farklı kullanmak istersne diye contactor durumlrı ve batarya max 
    info_labels.clear()
    
    for idx, (icon_text, label_text, value_text) in enumerate(info_items):

        row_container = QFrame()
        row_container.setStyleSheet('''
            QFrame {
                background-color: transparent;
                border: none;
                border-bottom: 1px solid #0077A8;
                padding: 10px 0px;
            }
        ''')
        
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(10, 5, 10, 5)
        row_layout.setSpacing(15)
        
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet(f"color: {accent_color}; font-size: 18px; background: transparent; border: none;")
        icon_label.setFixedWidth(30)
        row_layout.addWidget(icon_label)
        
        label = QLabel(label_text)
        label.setStyleSheet(f"color: {accent_color}; font-size: 16px; font-weight: bold; background: transparent; border: none;")
        label.setFixedWidth(220)
        row_layout.addWidget(label)
        
        value = QLabel(value_text)
        value.setStyleSheet("color: #ffffff; font-size: 16px; background: transparent; border: none;")
        info_labels.append(value)
        row_layout.addWidget(value)
        
        row_layout.addStretch()
        
        row_container.setLayout(row_layout)
        right_layout.addWidget(row_container)
    
    right_layout.addStretch()
    
    right_container.setLayout(right_layout)
    
    main_layout.addWidget(right_container, 1)  
    
    outer_layout = QVBoxLayout()
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer_layout.addLayout(main_layout)
    
    system_info_page.setLayout(outer_layout)
    
    return system_info_page

def update_system_info_display():   # sistem dueum bilgileri burada güncelelenecek. main.py de yeni bir liste tutacaksın ve bu listeye göre bu değereri güncelelyeceksin. Bu fonksiyonda güncelleeme yapacaksın
    pass
