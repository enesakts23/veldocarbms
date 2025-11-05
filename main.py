import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel, QStackedWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
import voltage
import temperature

app = QApplication(sys.argv)

current_page = "Voltage"

def update_button_styles():
    voltage_button.setStyleSheet("background-color: #007BFF; color: white;" if current_page == "Voltage" else "background-color: #333333; color: white;")
    temperature_button.setStyleSheet("background-color: #FF4500; color: white;" if current_page == "Temperature" else "background-color: #333333; color: white;")
    pack_view_button.setStyleSheet("background-color: #28A745; color: white;" if current_page == "Pack View" else "background-color: #333333; color: white;")
    config_button.setStyleSheet("background-color: #333333;" if current_page == "Configuration" else "background-color: #333333;")

window = QWidget()
window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
window.setGeometry(100, 100, 1000, 600)

header = QWidget()
header.setStyleSheet("background-color: #222222;")
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
voltage_button.setFixedSize(100, 40)
voltage_button.clicked.connect(lambda: [setattr(sys.modules[__name__], 'current_page', 'Voltage'), stacked_widget.setCurrentIndex(0), update_button_styles()])
header_layout.addWidget(voltage_button)

temperature_button = QPushButton("Temperature")
temperature_button.setFixedSize(100, 40)
temperature_button.clicked.connect(lambda: [setattr(sys.modules[__name__], 'current_page', 'Temperature'), stacked_widget.setCurrentIndex(1), update_button_styles()])
header_layout.addWidget(temperature_button)

pack_view_button = QPushButton("Pack View")
pack_view_button.setFixedSize(100, 40)
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

# Main area
main_area = QWidget()
main_area.setStyleSheet("background-color: black;")
main_area_layout = QVBoxLayout()
main_area_layout.setContentsMargins(0, 0, 0, 0)

# Stacked widget for pages
stacked_widget = QStackedWidget()

# Voltage page
voltage_page = voltage.create_voltage_page()
stacked_widget.addWidget(voltage_page)

# Temperature page
temperature_page = temperature.create_temperature_page()
stacked_widget.addWidget(temperature_page)

# Placeholder pages
pack_view_page = QWidget()
pack_view_page.setStyleSheet("background-color: black;")
stacked_widget.addWidget(pack_view_page)

config_page = QWidget()
config_page.setStyleSheet("background-color: black;")
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