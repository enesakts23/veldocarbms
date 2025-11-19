from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QRectF, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush
import random
import math

# Global lists to hold QLabel references for updating
voltage_labels = []

class VoltageCell(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("border: none;")
        self.error_mode = False
        self.high_temp_mode = False
        # Animation için wave offset ve timer
        self.wave_offset = 0
        self.repaint_timer = QTimer(self)
        self.repaint_timer.timeout.connect(self.update_animation)
        self.repaint_timer.start(80)  # 80ms'de bir güncelle
        self.voltage_label = QLabel("", self)
        self.voltage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.voltage_label.setGeometry(0, 0, self.width(), self.height())
        self.voltage_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 900; background: transparent;")
        voltage_labels.append(self.voltage_label)

        pole_w = 12
        pole_h = 12
        self.positive_pole = QLabel(self)
        self.positive_pole.setFixedSize(pole_w, pole_h)
        self.positive_pole.setStyleSheet(
            "background-color: #808080; border: 2px solid #606060; border-radius: 3px;"
        )
        self.positive_pole.move(3, - (pole_h // 2))

        self.negative_pole = QLabel(self)
        self.negative_pole.setFixedSize(pole_w, pole_h)
        self.negative_pole.setStyleSheet(
            "background-color: #808080; border: 2px solid #606060; border-radius: 3px;"
        )

    def set_error_mode(self, error):
        self.error_mode = error
        self.update()

    def set_high_temp_mode(self, high_temp):
        self.high_temp_mode = high_temp
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.error_mode:
            self.draw_error_background(painter)
        elif self.high_temp_mode:
            self.draw_wave_background(painter)
        else:
            painter.setBrush(QColor("#2b2b2b"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect(), 8, 8)

    def draw_error_background(self, painter):
        rect = self.rect()
        painter.setBrush(QColor("#2C2C2C"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)
        painter.setPen(QPen(QColor(0, 0, 0, 180), 2))
        
        line_spacing = 8
        
        start_x = rect.x() - rect.height()
        while start_x < rect.x() + rect.width():
            painter.drawLine(
                int(start_x), int(rect.y()),
                int(start_x + rect.height()), int(rect.y() + rect.height())
            )
            start_x += line_spacing

        start_x = rect.x() + rect.width() + rect.height()
        while start_x > rect.x() - rect.height():
            painter.drawLine(
                int(start_x), int(rect.y()),
                int(start_x - rect.height()), int(rect.y() + rect.height())
            )
            start_x -= line_spacing

    def draw_wave_background(self, painter):
        rect = self.rect()
        painter.setBrush(QBrush(QColor("#2C2C2C")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 8, 8)
        painter.setClipPath(path)
        
        wave_colors = [
            QColor(255, 0, 0, 120),    
            QColor(255, 80, 80, 90),   
            QColor(255, 150, 150, 60)  
        ]
        
        wave_heights = [rect.height() * 0.4, rect.height() * 0.3, rect.height() * 0.2]
        wave_speeds = [1.0, 1.8, 2.5]
        
        for i, (color, height, speed) in enumerate(zip(wave_colors, wave_heights, wave_speeds)):
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            wave_path = QPainterPath()
            start_x = rect.x()
            start_y = rect.y() + rect.height() - height
            
            wave_path.moveTo(start_x, start_y)
            
            for x in range(int(rect.width()) + 1):
                wave_x = start_x + x
                wave_y = start_y + height * 0.5 * math.sin((x * 0.1 + self.wave_offset * speed + i * math.pi / 3))
                wave_path.lineTo(wave_x, wave_y)
            
            wave_path.lineTo(rect.x() + rect.width(), rect.y() + rect.height())
            wave_path.lineTo(rect.x(), rect.y() + rect.height())
            wave_path.closeSubpath()
            
            painter.drawPath(wave_path)
        
        painter.setClipping(False)

    def update_animation(self):
        """Animation timer için güncelleme fonksiyonu"""
        self.wave_offset += 0.5  # Dalga hızını artırdık
        if self.wave_offset > 2 * math.pi:  # 2π
            self.wave_offset = 0
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.voltage_label.setGeometry(0, 0, self.width(), self.height())
        self.negative_pole.move(self.width() - (12 + 3), - (12 // 2))

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
        cell_widget = VoltageCell(module1_container)
        cell_widget.setFixedSize(cell_w, cell_h)
        cell_widget.move(x_pos, y_pos)
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
        cell_widget = VoltageCell(module2_container)
        cell_widget.setFixedSize(cell_w2, cell_h2)
        cell_widget.move(x_pos, y_pos)
    layout.addWidget(module2_container)
    
    return page

def update_voltage_display():
    import __main__ as main_mod
    error_mode = getattr(main_mod, 'error_flag', False)
    high_temp_mode = getattr(main_mod, 'high_temp_flag', False)
    high_temp_voltage_cells = getattr(main_mod, 'high_temp_voltage_cells', [])
    active_errors = getattr(main_mod, 'active_errors', [])
    critical_errors = ["Ic fail", "Open Wire", "Can Error"]
    error_text = ""
    for err in critical_errors:
        if err in active_errors:
            if err == "Ic fail":
                error_text = "IC F."
            elif err == "Open Wire":
                error_text = "O.W."
            elif err == "Can Error":
                error_text = "C.E."
            break
    for i in range(15):
        cell_widget = voltage_labels[i].parent()
        if hasattr(cell_widget, 'set_error_mode'):
            cell_widget.set_error_mode(error_mode)
        
        # High temperature mode kontrolü
        if hasattr(cell_widget, 'set_high_temp_mode'):
            is_high_temp = (i+1) in high_temp_voltage_cells if high_temp_mode else False
            cell_widget.set_high_temp_mode(is_high_temp)
        
        if error_mode:
            voltage_labels[i].setText(error_text)
        else:
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
