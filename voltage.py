from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt

def create_voltage_page():
    page = QWidget()
    page.setStyleSheet("background-color: #1a1a2e;")  # Koyu mavi-siyah arka plan

    layout = QGridLayout()
    layout.setSpacing(15)  # Daha fazla boşluk
    layout.setContentsMargins(30, 30, 30, 30)

    for i in range(15):
        voltage = 3.2 + i * 0.03
        
        # Voltaj seviyesine göre renk belirleme
        if voltage < 3.3:
            bg_color = "#ff6b6b"  # Kırmızı (düşük voltaj)
            border_color = "#ff4757"
        elif voltage > 3.8:
            bg_color = "#ffa726"  # Turuncu (yüksek voltaj)
            border_color = "#fb8c00"
        else:
            bg_color = "#4ecdc4"  # Yeşil (normal voltaj)
            border_color = "#26d0ce"
        
        cell = QLabel(f"{voltage:.2f} V")
        cell.setStyleSheet(f"""
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {bg_color}, stop:1 {bg_color}dd);
            color: white;
            border: 3px solid {border_color};
            border-radius: 15px;
            padding: 15px;
            font-size: 20px;
            font-weight: bold;
        """)
        cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Hover efekti için (PyQt6'da basit hover)
        cell.setToolTip(f"Cell {i+1}: {voltage:.2f} V")
        
        row = i // 3
        col = i % 3
        layout.addWidget(cell, row, col)

    page.setLayout(layout)
    return page
