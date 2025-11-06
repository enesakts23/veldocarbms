from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
import random

def create_voltage_page():

    page = QWidget()
    page.setStyleSheet("background-color: #000000;")
    page.setMinimumSize(1000, 540)
    layout = QVBoxLayout()
    layout.setSpacing(20)  
    layout.setContentsMargins(30, 30, 30, 30)
    page.setLayout(layout)
    
    # Ekran boyutuna göre hücre boyutlarını hesapla
    page_width = 1000 - 60  # margins çıkarıldıktan sonra
    page_height = 540 - 60
    cell_width = (page_width // 4) - 10  # 4 sütun için
    cell_height = min(cell_width * 1.5, (page_height // 4) - 10)  # dikey dikdörtgen
    
    # Module-1 Container
    module1_container = QFrame()
    # make container transparent so page background shows through
    module1_container.setStyleSheet('''
        QFrame {
            background: transparent;
            border-radius: 12px;
            border: 2px solid #00b294;
            padding: 12px;
        }
    ''')
    module1_layout = QVBoxLayout()
    module1_layout.setSpacing(10)
    module1_layout.setContentsMargins(10, 10, 10, 10)
    
    # Module-1 Cells (8 cells: side-by-side horizontal)
    module1_cells_layout = QHBoxLayout()
    module1_cells_layout.setSpacing(8)
    module1_cells_layout.setContentsMargins(0, 0, 0, 0)

    # compute per-cell size based on container available width
    container_padding = 30  # left+right padding inside module
    cell_spacing = 8
    container_inner_width = page_width - container_padding
    cell_w = max(48, int((container_inner_width - (cell_spacing * (8 - 1))) / 8))
    cell_h = int(cell_w * 1.8)

    for i in range(8):
        voltage = round(random.uniform(3.2, 3.6), 2)
        cell_label = QLabel(f"{voltage}V")
        cell_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # fixed size to create vertical rectangle look
        cell_label.setFixedSize(cell_w, cell_h)
        # fixed dark gray cell style to match black background
        cell_label.setStyleSheet(f"""
            QLabel {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2b2b2b, stop:1 #1f1f1f);
                color: #ffffff;
                font-size: 12px;
                font-weight: bold;
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.04);
                padding: 3px;
            }}
            QLabel:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #333333, stop:1 #222222);
                border-color: rgba(255,255,255,0.08);
            }}
        """)
        module1_cells_layout.addWidget(cell_label)

    module1_layout.addLayout(module1_cells_layout)
    module1_container.setLayout(module1_layout)
    layout.addWidget(module1_container)
    
    # Module-2 Container
    module2_container = QFrame()
    module2_container.setStyleSheet('''
        QFrame {
            background: transparent;
            border-radius: 12px;
            border: 2px solid #00b294;
            padding: 12px;
        }
    ''')
    module2_layout = QVBoxLayout()
    module2_layout.setSpacing(10)
    module2_layout.setContentsMargins(10, 10, 10, 10)
    
    # Module-2 Cells (8 cells: side-by-side horizontal)
    module2_cells_layout = QHBoxLayout()
    module2_cells_layout.setSpacing(8)
    module2_cells_layout.setContentsMargins(0, 0, 0, 0)

    # use same per-cell size as module1
    cell_w2 = cell_w
    cell_h2 = cell_h

    for i in range(8):
        voltage = round(random.uniform(3.2, 3.6), 2)
        cell_label = QLabel(f"{voltage}V")
        cell_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cell_label.setFixedSize(cell_w2, cell_h2)
        cell_label.setStyleSheet(f"""
            QLabel {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2b2b2b, stop:1 #1f1f1f);
                color: #ffffff;
                font-size: 12px;
                font-weight: bold;
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.04);
                padding: 3px;
            }}
            QLabel:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #333333, stop:1 #222222);
                border-color: rgba(255,255,255,0.08);
            }}
        """)
        module2_cells_layout.addWidget(cell_label)

    module2_layout.addLayout(module2_cells_layout)
    module2_container.setLayout(module2_layout)
    layout.addWidget(module2_container)
    
    return page
