import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel, QStackedWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
import voltage
import temperature
import packview
import configuration

app = QApplication(sys.argv)
current_page = "Voltage"  # default olarak voltage sayfası açılacak main.py başlatılıdığı zmaanç.

def update_button_styles():
    # Common colors
    accent = "#00b294"

    # Unselected button: transparent background, accent colored border, white text
    normal = f"""
    QPushButton {{
        background-color: transparent;
        color: #ffffff;
        border: 2px solid {accent};
        border-radius: 8px;
        padding: 0 20px;
    }}
    QPushButton:hover {{
        background-color: rgba(0,178,148,0.08);
    }}
    """

    # Selected button: filled with accent color, black text
    selected = f"""
    QPushButton {{
        background-color: {accent};
        color: #000000;
        border: 2px solid {accent};
        border-radius: 8px;
        padding: 0 20px;
    }}
    """

    voltage_button.setStyleSheet(selected if current_page == "Voltage" else normal)
    temperature_button.setStyleSheet(selected if current_page == "Temperature" else normal)
    pack_view_button.setStyleSheet(selected if current_page == "Pack View" else normal)
    # keep config button as icon-only (no text styling change)
    config_button.setStyleSheet("background-color: transparent; border: none;")

window = QWidget()
window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
window.setGeometry(100, 100, 1000, 540)

header = QWidget()
header.setStyleSheet("background-color: #000000;")
header.setFixedHeight(50)
header_layout = QHBoxLayout()
header_layout.setContentsMargins(0, 0, 0, 0)
header_layout.setSpacing(0)

logo_label = QLabel()
pixmap = QPixmap("veldologo.png")
scaled_pixmap = pixmap.scaledToHeight(50)
logo_label.setPixmap(scaled_pixmap)
logo_label.setFixedSize(100, 50)
header_layout.addWidget(logo_label)

spacer = QWidget()
spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
header_layout.addWidget(spacer)

voltage_button = QPushButton("Voltage")
voltage_button.setFixedSize(120, 40)
voltage_button.clicked.connect(lambda: [setattr(sys.modules[__name__], 'current_page', 'Voltage'), stacked_widget.setCurrentIndex(0), update_button_styles()])
header_layout.addWidget(voltage_button)

# Add spacing between buttons
header_layout.addSpacing(15)

temperature_button = QPushButton("Temperature")
temperature_button.setFixedSize(140, 40)
temperature_button.clicked.connect(lambda: [setattr(sys.modules[__name__], 'current_page', 'Temperature'), stacked_widget.setCurrentIndex(1), update_button_styles()])
header_layout.addWidget(temperature_button)

header_layout.addSpacing(15)

pack_view_button = QPushButton("Pack View")
pack_view_button.setFixedSize(140, 40)
pack_view_button.clicked.connect(lambda: [setattr(sys.modules[__name__], 'current_page', 'Pack View'), stacked_widget.setCurrentIndex(2), update_button_styles()])
header_layout.addWidget(pack_view_button)

config_button = QPushButton()
config_button.setIcon(QIcon("configuration.png"))
config_button.setIconSize(QSize(40, 40))
config_button.setFixedSize(50, 50)
config_button.setFlat(True)
config_button.clicked.connect(lambda: [setattr(sys.modules[__name__], 'current_page', 'Configuration'), stacked_widget.setCurrentIndex(3), update_button_styles()])
header_layout.addWidget(config_button)

power_button = QPushButton()
power_button.setIcon(QIcon("poweroff.png"))
power_button.setIconSize(QSize(40, 40))
power_button.setFixedSize(50, 50)
power_button.setFlat(True)
power_button.clicked.connect(app.quit)
header_layout.addWidget(power_button)
header.setLayout(header_layout)

update_button_styles()
main_area = QWidget()
main_area.setStyleSheet("background-color: #1a1a2e;")
main_area_layout = QVBoxLayout()
main_area_layout.setContentsMargins(0, 0, 0, 0)

stacked_widget = QStackedWidget()
voltage_page = voltage.create_voltage_page()
stacked_widget.addWidget(voltage_page)
temperature_page = temperature.create_temperature_page()
stacked_widget.addWidget(temperature_page)
pack_view_page = packview.create_pack_view_page()
stacked_widget.addWidget(pack_view_page)
config_page = configuration.create_configuration_page()
stacked_widget.addWidget(config_page)
main_area_layout.addWidget(stacked_widget)
main_area.setLayout(main_area_layout)
stacked_widget.setCurrentIndex(0)


layout = QVBoxLayout()
layout.setContentsMargins(0, 0, 0, 0)
layout.setSpacing(0)
layout.addWidget(header)
layout.addWidget(main_area)

window.setLayout(layout)
window.show()
sys.exit(app.exec())