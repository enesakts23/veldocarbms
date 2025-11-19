from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel, QVBoxLayout, QPushButton, QButtonGroup, QDialog
from PyQt6.QtCore import Qt, QTimer, QPointF, QPropertyAnimation, QEasingCurve, pyqtProperty, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QPolygonF, QFont
import math

# Global lists to hold QLabel references for updating
pack_labels = []
battery_widget = None
idl_button = None
chr_button = None
dsc_button = None
update_button_styles_func = None
switches = []
page = None


class AnimatedSwitch(QWidget):
    toggled = pyqtSignal(bool)
    
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.setFixedSize(50, 26)
        self._checked = False
        self._circle_position = 0
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(200)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    @pyqtProperty(int)
    def circle_position(self):
        return self._circle_position
    
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()
    
    def isChecked(self):
        return self._checked
    
    def setChecked(self, checked):
        if self._checked == checked:
            return
        self._checked = checked
        self.animation.stop()
        if checked:
            self.animation.setStartValue(self._circle_position)
            self.animation.setEndValue(24)
        else:
            self.animation.setStartValue(self._circle_position)
            self.animation.setEndValue(0)
        self.animation.start()
        self.toggled.emit(self._checked)
    
    def mousePressEvent(self, event):
        action = "activated" if not self._checked else "deactivated"
        dialog = ConfirmationDialog(f"{self.name} will be {action}, are you sure?", parent=page)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.setChecked(not self._checked)
        super().mousePressEvent(event)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background track
        if self._checked:
            track_color = QColor("#0077A8")
        else:
            track_color = QColor("#3a3a4e")
        
        painter.setBrush(QBrush(track_color))
        painter.setPen(QPen(QColor("#0077A8"), 2))
        painter.drawRoundedRect(0, 0, 50, 26, 13, 13)
        
        # Moving circle
        circle_color = QColor("#ffffff")
        painter.setBrush(QBrush(circle_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(self._circle_position + 3, 3, 20, 20)


class BatteryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.level = 0  # Veri yokken 0 göster
        self.setMinimumSize(120, 300)
        self.setMaximumWidth(160)

    def setLevel(self, soc):
        self.level = soc
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        body_left = int(w * 0.2)
        body_top = int(h * 0.08)
        body_width = int(w * 0.6)
        body_height = int(h * 0.8)

        painter.setPen(QPen(QColor("#3a3a4e"), 4))
        painter.setBrush(QBrush(QColor("#2a2a3e")))
        painter.drawRoundedRect(body_left, body_top, body_width, body_height, 15, 15)

        terminal_width = int(w * 0.24)
        terminal_height = int(h * 0.06)
        terminal_left = int(w * 0.38)
        terminal_top = int(h * 0.02)
        painter.setBrush(QBrush(QColor("#3a3a4e")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(terminal_left, terminal_top, terminal_width, terminal_height, 5, 5)

        soc = max(0, min(100, self.level))

        if soc > 0:
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

            fill_height_actual = fill_height * soc / 100
            fill_top_actual = fill_top + fill_height - fill_height_actual

            # Düz doluluk çizimi (wave olmadan)
            gradient = QLinearGradient(0, fill_top + fill_height, 0, fill_top_actual)
            gradient.setColorAt(0, color1)
            gradient.setColorAt(1, color2)

            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(fill_left, fill_top_actual, fill_width, fill_height_actual)

            shine_gradient = QLinearGradient(fill_left, 0, fill_left + fill_width * 0.4, 0)
            shine_gradient.setColorAt(0, QColor(255, 255, 255, 40))
            shine_gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.setBrush(QBrush(shine_gradient))
            shine_rect = [
                QPointF(fill_left, fill_top_actual),
                QPointF(fill_left + fill_width * 0.35, fill_top_actual),
                QPointF(fill_left + fill_width * 0.35, fill_top_actual + fill_height_actual),
                QPointF(fill_left, fill_top_actual + fill_height_actual)
            ]
            painter.drawPolygon(QPolygonF(shine_rect))

        painter.setPen(QPen(QColor("#ffffff"), 2))
        font = QFont("Arial", 24, QFont.Weight.Bold)
        painter.setFont(font)
        text_rect = painter.boundingRect(
            int(body_left), int(body_top + body_height / 2 - 20),
            int(body_width), 40,
            Qt.AlignmentFlag.AlignCenter,
            f"{soc:.0f}%"
        )
        if soc > 0:
            painter.setPen(QPen(QColor(0, 0, 0, 100), 3))
            painter.drawText(text_rect.adjusted(2, 2, 2, 2), Qt.AlignmentFlag.AlignCenter, f"{soc:.0f}%")
            painter.setPen(QPen(QColor("#ffffff"), 2))
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, f"{soc:.0f}%")


class ConfirmationDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmation")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #000000;
                color: #ffffff;
                border: 4px solid #0077A8;
                border-radius: 10px;
            }
        """)
        self.setModal(True)
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        label = QLabel(message)
        label.setStyleSheet("color: #ffffff; font-size: 14px; background: transparent;")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        yes_button = QPushButton("Yes")
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: #0077A8;
                color: #000000;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005577;
            }
        """)
        yes_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ffffff;
                border: 2px solid #0077A8;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 119, 168, 0.1);
            }
        """)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        self.setLayout(layout)


def create_pack_view_page():
    global idl_button, chr_button, dsc_button, update_button_styles_func, switches, page
    page = QWidget()
    page.setStyleSheet("background-color: #000000;")
    page.setMinimumSize(1000, 540)

    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(20)

    # Sol container (%55 yer kaplayacak)
    left_container = QFrame()
    left_container.setStyleSheet('''
        QFrame {
            background-color: transparent;
            border: 4px solid #0077A8;
            border-radius: 10px;
        }
    ''')
    left_container.setMinimumWidth(int(1000 * 0.53))
    left_container.setMaximumWidth(int(1000 * 0.57))

    # Sol container için layout
    left_layout = QVBoxLayout()
    left_layout.setContentsMargins(20, 20, 20, 20)
    left_layout.setSpacing(15)

    # Accent renk
    accent_color = "#0077A8"

    # Bilgi satırları - ikon ile birlikte
    info_items = [
        ("🔋", "SOC:", ""),
        ("❤️", "SOH:", ""),
        ("⚡", "Vpack:", ""),
        ("🔌", "State:", ""),
        ("⚡", "Current:", ""),
        ("📉", "Min Cell:", ""),
        ("📈", "Max Cell:", "")
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
        pack_labels.append(value)
        row_layout.addWidget(value)

        # Sağ tarafı doldur
        row_layout.addStretch()

        left_layout.addLayout(row_layout)

    left_container.setLayout(left_layout)

    # Sağ container (%45 yer kaplayacak)
    right_container = QFrame()
    right_container.setStyleSheet('''
        QFrame {
            background-color: transparent;
            border: none;
            border-radius: 10px;
        }
    ''')
    right_container.setMinimumWidth(int(1000 * 0.43))
    right_container.setMaximumWidth(int(1000 * 0.47))

    # Place battery centered in right container
    global battery_widget
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
            border: 4px solid #0077A8;
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
    
    # Initial style update
    update_button_styles()
    button_group.buttonClicked.connect(lambda: update_button_styles())
    
    update_button_styles_func = update_button_styles
    
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
    
    # Add 3 switches below charging icon
    right_layout.addSpacing(15)
    
    # Main switch container frame
    main_switch_container = QFrame()
    main_switch_container.setStyleSheet('''
        QFrame {
            background-color: transparent;
            border: none;
            padding: 10px;
        }
    ''')
    main_switch_container.setFixedWidth(400)
    
    main_switch_layout = QHBoxLayout()
    main_switch_layout.setContentsMargins(10, 8, 10, 8)
    main_switch_layout.setSpacing(25)
    
    # Switch names
    switch_names = ["Pre-Charge", "Charge", "Discharge"]
    
    switches.clear()
    # Create 3 individual switch containers
    for i in range(3):
        switch_container = QFrame()
        switch_container.setStyleSheet('''
            QFrame {
                background-color: transparent;
                border-radius: 10px;
                border: 2px solid #0077A8;
                padding: 8px;
            }
        ''')
        switch_container.setFixedSize(100, 70)
        
        switch_inner_layout = QVBoxLayout()
        switch_inner_layout.setContentsMargins(0, 0, 0, 0)
        switch_inner_layout.setSpacing(10)
        
        # Switch name label
        name_label = QLabel(switch_names[i])
        name_label.setStyleSheet("color: #0077A8; font-size: 10px; font-weight: bold; background: transparent; border: none; padding: 5px 0px;")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        switch_inner_layout.addWidget(name_label)
        
        # Switch widget
        switch = AnimatedSwitch(switch_names[i])
        switches.append(switch)
        switch_inner_layout.addWidget(switch, 0, Qt.AlignmentFlag.AlignCenter)
        
        switch_container.setLayout(switch_inner_layout)
        main_switch_layout.addWidget(switch_container)
    
    main_switch_container.setLayout(main_switch_layout)
    right_layout.addWidget(main_switch_container, 0, Qt.AlignmentFlag.AlignHCenter)
    
    right_layout.addStretch(1)
    right_container.setLayout(right_layout)

    main_layout.addWidget(left_container, 55)  # Sol container %55 ağırlık
    main_layout.addWidget(right_container, 45)  # Sağ container %45 ağırlık

    page.setLayout(main_layout)
    return page

def update_pack_display():
    import __main__ as main_mod
    keys = ["SOC", "SOH", "Vpack", "Bat_Status", "Current", "Min_Cell", "Max_Cell"]
    for i, key in enumerate(keys):
        if key in main_mod.pack_data:
            if key == "Bat_Status":
                # State'i buton durumuna göre belirle
                if idl_button and idl_button.isChecked():
                    state = "IDLE"
                elif chr_button and chr_button.isChecked():
                    state = "CHARGING"
                elif dsc_button and dsc_button.isChecked():
                    state = "DISCHARGING"
                else:
                    state = "UNKNOWN"
                pack_labels[i].setText(state)
            elif key == "Vpack":
                # Vpack için iki basamak göster
                vpack_str = main_mod.pack_data["Vpack"]
                try:
                    vpack_val = float(vpack_str.split()[0])
                    pack_labels[i].setText(f"{vpack_val:.2f} V")
                except ValueError:
                    pack_labels[i].setText(vpack_str)
            else:
                pack_labels[i].setText(main_mod.pack_data[key])
        else:
            pack_labels[i].setText("")
    
    # Update battery SOC
    if "SOC" in main_mod.pack_data:
        soc_str = main_mod.pack_data["SOC"]
        try:
            soc_value = int(soc_str.rstrip('%'))
            battery_widget.setLevel(soc_value)
        except ValueError:
            battery_widget.setLevel(0)
    else:
        battery_widget.setLevel(0)
    
    # Update button based on current value
    if "Current" in main_mod.pack_data:
        current_str = main_mod.pack_data["Current"]
        try:
            current_val = float(current_str.split()[0])
            if -0.05 <= current_val <= 0.05:
                idl_button.setChecked(True)
            elif current_val < -0.05:
                chr_button.setChecked(True)
            elif current_val > 0.05:
                dsc_button.setChecked(True)
            update_button_styles_func()
        except ValueError:
            pass