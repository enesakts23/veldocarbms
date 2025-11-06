from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt

def create_temperature_page():
    page = QWidget()
    page.setStyleSheet("background-color: #1a1a2e;")  # Koyu mavi-siyah arka plan

    layout = QGridLayout()
    layout.setSpacing(10)
    layout.setContentsMargins(20, 20, 20, 20)

    for i in range(15):
        temperature = 22.5 + i * 0.03
        cell = QLabel(f"{temperature:.2f}")
        cell.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #555555, stop:1 #333333);
            color: white;
            border: 2px solid #777777;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
        """)
        cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
        row = i // 3
        col = i % 3
        layout.addWidget(cell, row, col)

    page.setLayout(layout)
    return page
