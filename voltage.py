from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
import random

# Global lists to hold QLabel references for updating
voltage_labels = []

def create_voltage_page():

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

    container_padding = 30  
    cell_spacing = 8
    container_inner_width = page_width - container_padding
    cell_w = max(48, int((container_inner_width - (cell_spacing * (8 - 1))) / 8))
    cell_h = int(cell_w * 1.8)

    for i in range(8):
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
        """)
        voltage_label = QLabel("", cell_widget)
        voltage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        voltage_label.setGeometry(0, 0, cell_w, cell_h)
        voltage_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 900; background: transparent;")
        voltage_labels.append(voltage_label)

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

    cell_w2 = cell_w
    cell_h2 = cell_h

    for i in range(7):
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
        """)
        voltage_label = QLabel("", cell_widget)
        voltage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        voltage_label.setGeometry(0, 0, cell_w2, cell_h2)
        voltage_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 900; background: transparent;")
        voltage_labels.append(voltage_label)
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
        negative_pole.move(cell_w2 - (pole_w + 3), - (pole_h // 2))
    layout.addWidget(module2_container)
    
    return page

def update_voltage_display():
    import __main__ as main_mod
    for i in range(15):
        key = f"V{i+1}"
        if key in main_mod.voltage_data:
            voltage_str = main_mod.voltage_data[key]
            try:
                # Extract the numeric part and unit
                parts = voltage_str.split()
                if len(parts) >= 2:
                    voltage_value = float(parts[0])
                    unit = parts[1]
                    formatted_voltage = f"{voltage_value:.2f} {unit}"
                else:
                    formatted_voltage = voltage_str
            except ValueError:
                formatted_voltage = voltage_str
            voltage_labels[i].setText(formatted_voltage)
        else:
            voltage_labels[i].setText("")
