
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
import random

# Global lists to hold QLabel references for updating
temperature_labels = []

def create_temperature_page():

    page = QWidget()
    page.setStyleSheet("background-color: #000000;")
    page.setMinimumSize(1000, 540)
    layout = QVBoxLayout()
    layout.setSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30)
    page.setLayout(layout)
    page_width = 1000 - 60  
    page_height = 540 - 60
    cell_width = (page_width // 4) - 10  
    cell_height = min(cell_width * 1.5, (page_height // 4) - 10)  
    module1_container = QFrame()
    module1_container.setStyleSheet('''
        QFrame {
            background: transparent;
            border-radius: 12px;
            border: 4px solid #0077A8;
            padding: 12px;
        }
    ''')
    module1_layout = QVBoxLayout()
    module1_layout.setSpacing(10)
    module1_layout.setContentsMargins(10, 10, 10, 10)    
    module1_cells_layout = QHBoxLayout()
    module1_cells_layout.setSpacing(8)
    module1_cells_layout.setContentsMargins(0, 0, 0, 0)

    container_padding = 16  
    cell_spacing = 8
    container_inner_width = page_width - container_padding
    calculated_w = int((container_inner_width - (cell_spacing * (4 - 1))) / 4)
    cell_w = max(56, min(120, calculated_w))
    cell_h = int(cell_w * 1.5)

    for i in range(4):
        cell_widget = QWidget(module1_container)
        cell_widget.setFixedSize(cell_w, cell_h)
        cell_widget.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2b2b2b, stop:1 #1f1f1f);
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.04);
            }}
        """)
        cell_label = QLabel("", cell_widget)
        cell_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cell_label.setGeometry(0, 0, cell_w, cell_h)
        cell_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 900; background: transparent;")
        temperature_labels.append(cell_label)
        pole_w = 12
        pole_h = 12
        positive_pole = QLabel(cell_widget)
        positive_pole.setFixedSize(pole_w, pole_h)
        positive_pole.setStyleSheet(
            "background-color: #808080; border: 2px solid #606060; border-radius: 3px;"
        )
        positive_pole.move(3, - (pole_h // 2))
        negative_pole = QLabel(cell_widget)
        negative_pole.setFixedSize(pole_w, pole_h)
        negative_pole.setStyleSheet(
            "background-color: #808080; border: 2px solid #606060; border-radius: 3px;"
        )
        negative_pole.move(cell_w - (pole_w + 3), - (pole_h // 2))
        module1_cells_layout.addWidget(cell_widget)

    module1_layout.addLayout(module1_cells_layout)
    module1_container.setLayout(module1_layout)
    layout.addWidget(module1_container)
    
    module2_container = QFrame()
    module2_container.setStyleSheet('''
        QFrame {
            background: transparent;
            border-radius: 12px;
            border: 4px solid #0077A8;
            padding: 12px;
        }
    ''')
    module2_layout = QVBoxLayout()
    module2_layout.setSpacing(10)
    module2_layout.setContentsMargins(10, 10, 10, 10)
    module2_cells_layout = QHBoxLayout()
    module2_cells_layout.setSpacing(8)
    module2_cells_layout.setContentsMargins(0, 0, 0, 0)

    cell_w2 = cell_w
    cell_h2 = cell_h

    for i in range(3):
        cell_widget = QWidget(module2_container)
        cell_widget.setFixedSize(cell_w2, cell_h2)
        cell_widget.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2b2b2b, stop:1 #1f1f1f);
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.04);
            }}
        """)
        cell_label = QLabel("", cell_widget)
        cell_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cell_label.setGeometry(0, 0, cell_w2, cell_h2)
        cell_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 900; background: transparent;")
        temperature_labels.append(cell_label)
        if i != 2:  # Sadece 3. hücre için kutup başları olmayacak
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
        module2_cells_layout.addWidget(cell_widget)

        module2_layout.addLayout(module2_cells_layout)
    module2_container.setLayout(module2_layout)
    layout.addWidget(module2_container)
    
    return page

def update_temperature_display():
    import __main__ as main_mod
    keys = ["T1", "T2", "T3", "T4", "T5", "T6", "TPCB"]
    for i, key in enumerate(keys):
        if key in main_mod.temperature_data:
            temperature_labels[i].setText(main_mod.temperature_data[key])
        else:
            temperature_labels[i].setText("")