from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

def create_configuration_page():
    page = QWidget()
    page.setStyleSheet("background-color: #1a1a2e;")  # Koyu mavi-siyah arka plan

    layout = QVBoxLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)

    title = QLabel("Configuration Settings")
    title.setStyleSheet("""
        color: white;
        font-size: 24px;
        font-weight: bold;
    """)
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)

    # Örnek ayarlar
    settings = [
        ("Max Voltage", "4.2"),
        ("Min Voltage", "2.5"),
        ("Max Temperature", "60"),
        ("Min Temperature", "0")
    ]

    for label_text, default_value in settings:
        label = QLabel(label_text)
        label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(label)

        input_field = QLineEdit(default_value)
        input_field.setStyleSheet("""
            background-color: #333333;
            color: white;
            border: 2px solid #777777;
            border-radius: 5px;
            padding: 5px;
            font-size: 16px;
        """)
        layout.addWidget(input_field)

    save_button = QPushButton("Save Settings")
    save_button.setStyleSheet("""
        background-color: #4ecdc4;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
    """)
    layout.addWidget(save_button)

    page.setLayout(layout)
    return page