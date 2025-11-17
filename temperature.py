from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush
import random
import math
from PyQt6.QtCore import QTimer

# Global lists to hold QLabel references for updating
temperature_labels = []

class TemperatureCell(QFrame):
    def __init__(self, parent=None, has_poles=True):
        super().__init__(parent)
        self.setStyleSheet("border: none;")
        self.error_mode = False
        self.high_temp_mode = False
        # Animation için wave offset ve timer
        self.wave_offset = 0
        self.repaint_timer = QTimer(self)
        self.repaint_timer.timeout.connect(self.update_animation)
        self.repaint_timer.start(80)  # 80ms'de bir güncelle
        self.cell_label = QLabel("", self)
        self.cell_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cell_label.setGeometry(0, 0, self.width(), self.height())
        self.cell_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 900; background: transparent;")
        temperature_labels.append(self.cell_label)

        if has_poles:
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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.cell_label.setGeometry(0, 0, self.width(), self.height())
        if hasattr(self, 'negative_pole'):
            self.negative_pole.move(self.width() - (12 + 3), - (12 // 2))

    def update_animation(self):
        """Animation timer için güncelleme fonksiyonu"""
        self.wave_offset += 0.5  # Dalga hızını artırdık
        if self.wave_offset > 2 * math.pi:  # 2π
            self.wave_offset = 0
        self.update()

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
        cell_widget = TemperatureCell(module1_container)
        cell_widget.setFixedSize(cell_w, cell_h)
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
        has_poles = (i != 2)
        cell_widget = TemperatureCell(module2_container, has_poles=has_poles)
        cell_widget.setFixedSize(cell_w2, cell_h2)
        module2_cells_layout.addWidget(cell_widget)

    module2_layout.addLayout(module2_cells_layout)
    module2_container.setLayout(module2_layout)
    layout.addWidget(module2_container)
    
    return page

def update_temperature_display():
    import __main__ as main_mod
    error_mode = getattr(main_mod, 'error_flag', False)
    high_temp_mode = getattr(main_mod, 'high_temp_flag', False)
    high_temp_widgets = getattr(main_mod, 'high_temp_widgets', [])
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
    keys = ["T1", "T2", "T3", "T4", "T5", "T6", "TPCB"]
    for i, key in enumerate(keys):
        cell_widget = temperature_labels[i].parent()
        if hasattr(cell_widget, 'set_error_mode'):
            cell_widget.set_error_mode(error_mode)
        if hasattr(cell_widget, 'set_high_temp_mode'):
            is_high_temp = (i+1) in high_temp_widgets if high_temp_mode else False
            cell_widget.set_high_temp_mode(is_high_temp)
        if error_mode:
            temperature_labels[i].setText(error_text)
        elif is_high_temp:
            temperature_labels[i].setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 900; background: transparent;")
            temperature_labels[i].setText(main_mod.temperature_data.get(key, ""))
        else:
            temperature_labels[i].setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 900; background: transparent;")
            temperature_labels[i].setText(main_mod.temperature_data.get(key, ""))