from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar, QPushButton, QButtonGroup
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QPolygonF, QFont
import math


class BatteryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.level = 85  # Sabit SOC %
        # Reduce vertical footprint so battery doesn't occupy the entire column
        self.setMinimumSize(120, 300)
        self.setMaximumWidth(160)
        self.wave_phase = 0
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
        
        # Pil gövdesi - daha koyu ve modern
        body_left = w * 0.2
        body_top = h * 0.08
        body_width = w * 0.6
        body_height = h * 0.8
        
        # Gövde dış çerçeve (koyu ton)
        painter.setPen(QPen(QColor("#3a3a4e"), 4))
        painter.setBrush(QBrush(QColor("#2a2a3e")))
        painter.drawRoundedRect(body_left, body_top, body_width, body_height, 15, 15)
        
        # Pil başı (terminal)
        terminal_width = w * 0.24
        terminal_height = h * 0.06
        terminal_left = w * 0.38
        terminal_top = h * 0.02
        painter.setBrush(QBrush(QColor("#3a3a4e")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(terminal_left, terminal_top, terminal_width, terminal_height, 5, 5)
        
        # Seviye hesaplama
        soc = max(0, min(100, self.level))
        
        # Renk belirleme (gradient)
        if soc > 30:
            color1 = QColor("#4caf50")
            color2 = QColor("#8bc34a")
        elif soc > 10:
            color1 = QColor("#ff9800")
            color2 = QColor("#ffb300")
        else:
            color1 = QColor("#f44336")
            color2 = QColor("#ff5252")
        
        # İç dolgu alanı
        fill_left = body_left + 6
        fill_top = body_top + 6
        fill_width = body_width - 12
        fill_height = body_height - 12
        
        # Dalga üst sınırı
        wave_height = fill_height * soc / 100
        wave_top = fill_top + fill_height - wave_height
        
        # Dalga noktaları oluştur
        wave_points = []
        for i in range(0, int(fill_width) + 1, 2):
            x = fill_left + i
            y = wave_top + 8 * math.sin((i / 22.0) + self.wave_phase)
            wave_points.append((x, y))
        
        # Polygon: dalga + kenarlar + alt
        poly_points = []
        poly_points.extend(wave_points)
        poly_points.append((fill_left + fill_width, fill_top + fill_height))
        poly_points.append((fill_left, fill_top + fill_height))
        
        # Gradient dolgu
        gradient = QLinearGradient(0, fill_top + fill_height, 0, wave_top)
        gradient.setColorAt(0, color1)
        gradient.setColorAt(1, color2)
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(QPolygonF([QPointF(x, y) for x, y in poly_points]))
        
        # Parlama efekti (sol taraf)
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
        
        # SOC yazısı (merkeze, daha büyük ve kalın)
        painter.setPen(QPen(QColor("#ffffff"), 2))
        font = QFont("Arial", 24, QFont.Weight.Bold)
        painter.setFont(font)
        text_rect = painter.boundingRect(
            int(body_left), int(body_top + body_height / 2 - 20),
            int(body_width), 40,
            Qt.AlignmentFlag.AlignCenter,
            f"{soc:.0f}%"
        )
        # Gölge efekti
        painter.setPen(QPen(QColor(0, 0, 0, 100), 3))
        painter.drawText(text_rect.adjusted(2, 2, 2, 2), Qt.AlignmentFlag.AlignCenter, f"{soc:.0f}%")
        # Ana yazı
        painter.setPen(QPen(QColor("#ffffff"), 2))
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, f"{soc:.0f}%")


def create_pack_view_page():
    page = QWidget()
    # Set solid black background to match the rest of the app
    page.setStyleSheet("background-color: #000000;")
    page.setMinimumSize(1000, 540)
    
    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(20)

    # Sol: Yatay dikdörtgen container (ekranın %60'ı)
    left_container = QFrame()
    # Make container background transparent and use the accent border color
    left_container.setStyleSheet('''
        QFrame#mainleft {
            background-color: transparent;
            border-radius: 18px;
            border: 2px solid #00b294;
            padding: 24px 32px;
        }
    ''')
    left_container.setObjectName("mainleft")
    # Yüksekliği azalt, genişliği artır
    left_container.setMinimumHeight(240)
    left_container.setMaximumHeight(340)
    left_container.setMinimumWidth(int(1000*0.58))
    left_container.setMaximumWidth(int(1000*0.62))

    left_layout = QVBoxLayout()
    left_layout.setSpacing(12)
    left_layout.setContentsMargins(20, 16, 20, 16)

    def info_box(text, color, fsize=18, bold=True):
        box = QFrame()
        box.setStyleSheet(f'''
            QFrame {{
                background-color: rgba(255,255,255,0.10);
                border-radius: 8px;
                border-left: 4px solid {color};
                margin-bottom: 0px;
            }}
        ''')
        layout = QHBoxLayout()
        layout.setContentsMargins(14, 6, 14, 6)
        label = QLabel(text)
        label.setStyleSheet(f"color: {color}; font-size: {fsize}px; font-weight: {'bold' if bold else 'normal'}; background: transparent;")
        label.setMinimumHeight(28)
        layout.addWidget(label)
        box.setLayout(layout)
        return box

    left_layout.addWidget(info_box("SOC: 75%", "#4caf50", 22))
    left_layout.addWidget(info_box("SOH: 95%", "#00bcd4", 20))
    left_layout.addWidget(info_box("State: Discharge", "#ffb300", 18))
    left_layout.addWidget(info_box("Current: 10.0 A", "#fff", 18, False))
    left_layout.addWidget(info_box("Charge FET: ON   Discharge FET: ON", "#fff", 16, False))
    left_layout.addWidget(info_box("Min Cell: 3.872 V", "#b2ff59", 16, False))
    left_layout.addWidget(info_box("Max Cell: 3.876 V", "#ffd54f", 16, False))
    left_layout.addWidget(info_box("Delta: 0.001 V", "#fff", 16, False))

    left_layout.addStretch(1)
    left_container.setLayout(left_layout)

    # Sağ: Pil animasyonu (ekranın %40'ı)
    battery_widget = BatteryWidget()
    battery_widget.setMinimumWidth(int(1000*0.12))
    battery_widget.setMaximumWidth(int(1000*0.22))

    # Right column: stack battery and a bottom button container
    right_column = QFrame()
    right_column.setStyleSheet('background-color: transparent;')
    right_layout = QVBoxLayout()
    right_layout.setContentsMargins(0, 0, 0, 0)
    right_layout.setSpacing(8)

    # Center battery and place a compact button group immediately below it
    right_layout.addStretch(1)
    right_layout.addWidget(battery_widget, 0, Qt.AlignmentFlag.AlignHCenter)
    right_layout.addSpacing(12)

    # Compact button container directly under battery
    mode_frame = QFrame()
    mode_frame.setStyleSheet('''
        QFrame {
            background-color: transparent;
            border-radius: 10px;
            border: 2px solid #00b294;
            padding: 6px;
        }
    ''')
    mode_frame.setFixedHeight(56)
    mode_layout = QHBoxLayout()
    mode_layout.setContentsMargins(8, 4, 8, 4)
    mode_layout.setSpacing(8)

    dsc_button = QPushButton("DSC")
    idl_button = QPushButton("IDL")
    chr_button = QPushButton("CHR")

    # Make buttons checkable and small (compact segmented control look)
    for btn in (dsc_button, idl_button, chr_button):
        btn.setCheckable(True)
        btn.setFixedSize(68, 40)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

    # Styles
    accent = "#00b294"
    normal_btn_style = f"""
    QPushButton {{
        background-color: transparent;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: rgba(0,178,148,0.06);
    }}
    """
    selected_btn_style = f"""
    QPushButton {{
        background-color: {accent};
        color: #000000;
        border: 2px solid {accent};
        border-radius: 6px;
        font-weight: bold;
    }}
    """

    # Exclusive group so only one is checked
    btn_group = QButtonGroup(mode_frame)
    btn_group.setExclusive(True)
    btn_group.addButton(dsc_button)
    btn_group.addButton(idl_button)
    btn_group.addButton(chr_button)

    # Default to IDL
    idl_button.setChecked(True)

    def update_mode_styles():
        for b in (dsc_button, idl_button, chr_button):
            b.setStyleSheet(selected_btn_style if b.isChecked() else normal_btn_style)

    # Update styles initially and when clicked
    update_mode_styles()
    btn_group.buttonClicked.connect(lambda _: update_mode_styles())

    mode_layout.addWidget(dsc_button)
    mode_layout.addWidget(idl_button)
    mode_layout.addWidget(chr_button)
    mode_frame.setLayout(mode_layout)

    right_layout.addWidget(mode_frame, 0, Qt.AlignmentFlag.AlignHCenter)
    right_layout.addStretch(1)
    right_column.setLayout(right_layout)

    main_layout.addWidget(left_container, 3)
    main_layout.addWidget(right_column, 2)
    page.setLayout(main_layout)
    return page