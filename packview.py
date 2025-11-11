from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel, QVBoxLayout, QPushButton, QButtonGroup
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QPolygonF, QFont
import math


class BatteryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.level = 85  # example SOC
        self.setMinimumSize(120, 300)
        self.setMaximumWidth(160)
        self.wave_phase = 0.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_wave)
        self.timer.start(40)

    def animate_wave(self):
        self.wave_phase += 0.18
        self.update()

    def setLevel(self, soc):
        self.level = soc
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        body_left = w * 0.2
        body_top = h * 0.08
        body_width = w * 0.6
        body_height = h * 0.8

        painter.setPen(QPen(QColor("#3a3a4e"), 4))
        painter.setBrush(QBrush(QColor("#2a2a3e")))
        painter.drawRoundedRect(body_left, body_top, body_width, body_height, 15, 15)

        terminal_width = w * 0.24
        terminal_height = h * 0.06
        terminal_left = w * 0.38
        terminal_top = h * 0.02
        painter.setBrush(QBrush(QColor("#3a3a4e")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(terminal_left, terminal_top, terminal_width, terminal_height, 5, 5)

        soc = max(0, min(100, self.level))

        if soc > 30:
            color1 = QColor("#00b51a")
            color2 = QColor("#00b51a")
        elif soc > 10:
            color1 = QColor("#ff9800")
            color2 = QColor("#ffb300")
        else:
            color1 = QColor("#f44336")
            color2 = QColor("#ff5252")

        fill_left = body_left + 6
        fill_top = body_top + 6
        fill_width = body_width - 12
        fill_height = body_height - 12

        wave_height = fill_height * soc / 100
        wave_top = fill_top + fill_height - wave_height

        wave_points = []
        for i in range(0, int(fill_width) + 1, 2):
            x = fill_left + i
            y = wave_top + 8 * math.sin((i / 22.0) + self.wave_phase)
            wave_points.append((x, y))

        poly_points = []
        poly_points.extend(wave_points)
        poly_points.append((fill_left + fill_width, fill_top + fill_height))
        poly_points.append((fill_left, fill_top + fill_height))

        gradient = QLinearGradient(0, fill_top + fill_height, 0, wave_top)
        gradient.setColorAt(0, color1)
        gradient.setColorAt(1, color2)

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(QPolygonF([QPointF(x, y) for x, y in poly_points]))

        shine_gradient = QLinearGradient(fill_left, 0, fill_left + fill_width * 0.4, 0)
        shine_gradient.setColorAt(0, QColor(255, 255, 255, 40))
        shine_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(shine_gradient))
        shine_poly = [
            QPointF(fill_left, fill_top),
            QPointF(fill_left + fill_width * 0.35, fill_top),
            QPointF(fill_left + fill_width * 0.35, fill_top + fill_height),
            QPointF(fill_left, fill_top + fill_height)
        ]
        painter.drawPolygon(QPolygonF(shine_poly))

        painter.setPen(QPen(QColor("#ffffff"), 2))
        font = QFont("Arial", 24, QFont.Weight.Bold)
        painter.setFont(font)
        text_rect = painter.boundingRect(
            int(body_left), int(body_top + body_height / 2 - 20),
            int(body_width), 40,
            Qt.AlignmentFlag.AlignCenter,
            f"{soc:.0f}%"
        )
        painter.setPen(QPen(QColor(0, 0, 0, 100), 3))
        painter.drawText(text_rect.adjusted(2, 2, 2, 2), Qt.AlignmentFlag.AlignCenter, f"{soc:.0f}%")
        painter.setPen(QPen(QColor("#ffffff"), 2))
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, f"{soc:.0f}%")

def create_pack_view_page():
    page = QWidget()
    page.setStyleSheet("background-color: #000000;")
    page.setMinimumSize(1000, 540)

    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(20)

    # Sol container (%70 yer kaplayacak)
    left_container = QFrame()
    left_container.setStyleSheet('''
        QFrame {
            background-color: transparent;
            border: 2px solid #00b51a;
            border-radius: 10px;
        }
    ''')
    left_container.setMinimumWidth(int(1000 * 0.68))
    left_container.setMaximumWidth(int(1000 * 0.72))

    # Sol container için layout
    left_layout = QVBoxLayout()
    left_layout.setContentsMargins(20, 20, 20, 20)
    left_layout.setSpacing(15)

    # Accent renk
    accent_color = "#00b51a"

    # Bilgi satırları - ikon ile birlikte
    info_items = [
        ("🔋", "SOC:", "85.00%"),
        ("❤️", "SOH:", "100.00%"),
        ("🔌", "State:", "IDLE"),
        ("⚡", "Current:", "0.00 A"),
        ("📉", "Min Cell:", "0.00 V"),
        ("📈", "Max Cell:", "0.00 V")
    ]

    for icon_text, label_text, value_text in info_items:
        # Yatay layout için her satır
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)

        # İkon
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet(f"color: {accent_color}; font-size: 18px; background: transparent; border: none;")
        row_layout.addWidget(icon_label)

        # Etiket (isim) - accent renk
        label = QLabel(label_text)
        label.setStyleSheet(f"color: {accent_color}; font-size: 16px; font-weight: bold; background: transparent; border: none;")
        row_layout.addWidget(label)

        # Değer - beyaz renk
        value = QLabel(value_text)
        value.setStyleSheet("color: #ffffff; font-size: 16px; background: transparent; border: none;")
        row_layout.addWidget(value)

        # Sağ tarafı doldur
        row_layout.addStretch()

        left_layout.addLayout(row_layout)

    left_container.setLayout(left_layout)

    # Sağ container (%30 yer kaplayacak)
    right_container = QFrame()
    right_container.setStyleSheet('''
        QFrame {
            background-color: transparent;
            border: none;
            border-radius: 10px;
        }
    ''')
    right_container.setMinimumWidth(int(1000 * 0.28))
    right_container.setMaximumWidth(int(1000 * 0.32))

    # Place battery centered in right container
    battery_widget = BatteryWidget()
    right_layout = QVBoxLayout()
    right_layout.setContentsMargins(12, 12, 12, 12)
    right_layout.addStretch(1)
    right_layout.addWidget(battery_widget, 0, Qt.AlignmentFlag.AlignHCenter)
    
    # Oval button group below battery
    button_frame = QFrame()
    button_frame.setStyleSheet('''
        QFrame {
            background-color: transparent;
            border-radius: 15px;
            border: 2px solid #00b51a;
            padding: 1px;
        }
    ''')
    button_frame.setFixedHeight(32)
    button_frame.setFixedWidth(140)  # Butonları çevrelemek için sabit genişlik (biraz daha sıkı)
    
    button_layout = QHBoxLayout()
    # biraz soldan daraltmak için sol margin'i azalt
    button_layout.setContentsMargins(2, 1, 4, 1)
    button_layout.setSpacing(3)
    
    # Create buttons
    dsc_button = QPushButton("DSC")
    idl_button = QPushButton("IDL")
    chr_button = QPushButton("CHR")
    
    # Make buttons checkable and oval
    for btn in (dsc_button, idl_button, chr_button):
        btn.setCheckable(True)
        btn.setFixedSize(45, 22)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
    
    # Button styles
    # Use a pill-shaped radius equal to half the button height (button height = 22 -> radius = 11)
    normal_style = f"""
    QPushButton {{
        background-color: transparent;
        color: #ffffff;
        border: 2px solid transparent;
        border-radius: 11px; /* pill */
        font-weight: bold;
        font-size: 12px;
    }}
    QPushButton:hover {{
        background-color: rgba(0,181,26,0.08);
    }}
    """
    
    selected_style = f"""
    QPushButton {{
        background-color: {accent_color};
        color: #000000;
        border: 2px solid {accent_color};
        border-radius: 11px; /* pill */
        font-weight: bold;
        font-size: 12px;
    }}
    """
    
    # Button group for exclusive selection
    button_group = QButtonGroup(button_frame)
    button_group.setExclusive(True)
    button_group.addButton(dsc_button)
    button_group.addButton(idl_button)
    button_group.addButton(chr_button)
    
    # Default to IDL (middle button)
    idl_button.setChecked(True)
    
    # Charging icon below buttons (only visible when CHR is selected)
    charging_icon = QLabel("⚡")
    charging_icon.setStyleSheet("color: #00b51a; font-size: 24px; background: transparent; border: none;")
    charging_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    charging_icon.setVisible(False)  # Initially hidden
    
    def update_button_styles():
        for b in (dsc_button, idl_button, chr_button):
            b.setStyleSheet(selected_style if b.isChecked() else normal_style)
        
        # Show/hide charging icon based on CHR selection
        charging_icon.setVisible(chr_button.isChecked())
    
    # Initial style update
    update_button_styles()
    button_group.buttonClicked.connect(lambda: update_button_styles())
    
    button_layout.addStretch()
    button_layout.addWidget(dsc_button)
    button_layout.addWidget(idl_button)
    button_layout.addWidget(chr_button)
    button_layout.addStretch()
    button_frame.setLayout(button_layout)
    
    right_layout.addSpacing(3)
    right_layout.addWidget(button_frame, 0, Qt.AlignmentFlag.AlignHCenter)
    right_layout.addSpacing(5)
    right_layout.addWidget(charging_icon, 0, Qt.AlignmentFlag.AlignHCenter)
    right_layout.addStretch(1)
    right_container.setLayout(right_layout)

    main_layout.addWidget(left_container, 7)  # Sol container %70 ağırlık
    main_layout.addWidget(right_container, 3)  # Sağ container %30 ağırlık

    page.setLayout(main_layout)
    return page