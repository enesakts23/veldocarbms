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
            border: 2px solid #00b51a;
            padding: 12px;
        }
    ''')
    # module1_container: don't set a layout so we can position children absolutely
    
    # compute per-cell size based on container available width
    container_padding = 30  # left+right padding inside module
    cell_spacing = 8
    container_inner_width = page_width - container_padding
    cell_w = max(48, int((container_inner_width - (cell_spacing * (8 - 1))) / 8))
    cell_h = int(cell_w * 1.8)

    for i in range(8):
        voltage = round(random.uniform(3.2, 3.6), 2)
        x_pos = 10 + i * (cell_w + cell_spacing)
        y_pos = 20
        cell_widget = QWidget(module1_container)
        cell_widget.setFixedSize(cell_w, cell_h)
        cell_widget.move(x_pos, y_pos)
        cell_widget.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2b2b2b, stop:1 #1f1f1f);
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.04);
            }}
            QWidget:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #333333, stop:1 #222222);
                border-color: rgba(255,255,255,0.08);
            }}
        """)
        voltage_label = QLabel(f"{voltage}V", cell_widget)
        voltage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        voltage_label.setGeometry(0, 0, cell_w, cell_h)
        voltage_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 900; background: transparent;")
        # Pozitif kutup başı (sol üst)
        pole_w = 12
        pole_h = 12
        positive_pole = QLabel(cell_widget)
        positive_pole.setFixedSize(pole_w, pole_h)
        positive_pole.setStyleSheet(
            "background-color: #808080; border: 2px solid #606060; border-radius: 3px;"
        )
        positive_pole.move(3, - (pole_h // 2))
        # Negatif kutup başı (sağ üst)
        negative_pole = QLabel(cell_widget)
        negative_pole.setFixedSize(pole_w, pole_h)
        negative_pole.setStyleSheet(
            "background-color: #808080; border: 2px solid #606060; border-radius: 3px;"
        )
        negative_pole.move(cell_w - (pole_w + 3), - (pole_h // 2))
    layout.addWidget(module1_container)
    
    # Module-2 Container
    module2_container = QFrame()
    module2_container.setStyleSheet('''
        QFrame {
            background: transparent;
            border-radius: 12px;
            border: 2px solid #00b51a;
            padding: 12px;
        }
    ''')
    # module2_container: don't set a layout so we can position children absolutely
    
    # use same per-cell size as module1
    cell_w2 = cell_w
    cell_h2 = cell_h

    for i in range(8):
        voltage = round(random.uniform(3.2, 3.6), 2)
        x_pos = 10 + i * (cell_w2 + cell_spacing)
        y_pos = 20
        cell_widget = QWidget(module2_container)
        cell_widget.setFixedSize(cell_w2, cell_h2)
        cell_widget.move(x_pos, y_pos)
        cell_widget.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2b2b2b, stop:1 #1f1f1f);
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.04);
            }}
            QWidget:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #333333, stop:1 #222222);
                border-color: rgba(255,255,255,0.08);
            }}
        """)
        voltage_label = QLabel(f"{voltage}V", cell_widget)
        voltage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        voltage_label.setGeometry(0, 0, cell_w2, cell_h2)
        voltage_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 900; background: transparent;")
        # Pozitif kutup başı (sol üst)
        pole_w = 12
        pole_h = 12
        positive_pole = QLabel(cell_widget)
        positive_pole.setFixedSize(pole_w, pole_h)
        positive_pole.setStyleSheet(
            "background-color: #808080; border: 2px solid #606060; border-radius: 3px;"
        )
        positive_pole.move(3, - (pole_h // 2))
        # Negatif kutup başı (sağ üst)
        negative_pole = QLabel(cell_widget)
        negative_pole.setFixedSize(pole_w, pole_h)
        negative_pole.setStyleSheet(
            "background-color: #808080; border: 2px solid #606060; border-radius: 3px;"
        )
        negative_pole.move(cell_w2 - (pole_w + 3), - (pole_h // 2))
    layout.addWidget(module2_container)
    
    return page
