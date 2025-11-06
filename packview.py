from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt

def create_pack_view_page():
    page = QWidget()
    page.setStyleSheet("background-color: #1a1a2e;")  # Koyu mavi-siyah arka plan

    layout = QGridLayout()
    layout.setSpacing(10)
    layout.setContentsMargins(20, 20, 20, 20)

    # Pack view için örnek widgetlar
    pack_label = QLabel("Pack Overview")
    pack_label.setStyleSheet("""
        color: white;
        font-size: 24px;
        font-weight: bold;
    """)
    pack_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(pack_label, 0, 0, 1, 3)

    for i in range(5):
        pack_info = QLabel(f"Pack {i+1}: OK")
        pack_info.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4ecdc4, stop:1 #26d0ce);
            color: white;
            border: 2px solid #26d0ce;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
        """)
        pack_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(pack_info, i+1, 0, 1, 3)

    page.setLayout(layout)
    return page