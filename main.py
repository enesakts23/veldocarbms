import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

app = QApplication(sys.argv)

window = QWidget()
window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
window.setGeometry(100, 100, 1000, 600)

# Header
header = QWidget()
header.setStyleSheet("background-color: #222222;")
header.setFixedHeight(50)

# Header layout
header_layout = QHBoxLayout()
header_layout.setContentsMargins(0, 0, 0, 0)
header_layout.setSpacing(0)

# Logo
logo_label = QLabel()
pixmap = QPixmap("veldologo.png")
scaled_pixmap = pixmap.scaledToHeight(50)
logo_label.setPixmap(scaled_pixmap)
logo_label.setFixedSize(100, 50)
header_layout.addWidget(logo_label)

# Spacer to push buttons to the right
spacer = QWidget()
spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
header_layout.addWidget(spacer)

# Voltage button
voltage_button = QPushButton("Voltage")
voltage_button.setFixedSize(100, 40)
header_layout.addWidget(voltage_button)

# Temperature button
temperature_button = QPushButton("Temperature")
temperature_button.setFixedSize(100, 40)
header_layout.addWidget(temperature_button)

# Pack View button
pack_view_button = QPushButton("Pack View")
pack_view_button.setFixedSize(100, 40)
header_layout.addWidget(pack_view_button)

# Configuration button
config_button = QPushButton()
config_button.setIcon(QIcon("configuration.png"))
config_button.setIconSize(QSize(40, 40))
config_button.setFixedSize(50, 50)
config_button.setFlat(True)
header_layout.addWidget(config_button)

# Power off button
power_button = QPushButton()
power_button.setIcon(QIcon("poweroff.png"))
power_button.setIconSize(QSize(40, 40))
power_button.setFixedSize(50, 50)
power_button.setFlat(True)
power_button.clicked.connect(app.quit)
header_layout.addWidget(power_button)

header.setLayout(header_layout)

# Main area
main_area = QWidget()
main_area.setStyleSheet("background-color: black;")

# Layout
layout = QVBoxLayout()
layout.setContentsMargins(0, 0, 0, 0)
layout.setSpacing(0)
layout.addWidget(header)
layout.addWidget(main_area)

window.setLayout(layout)
window.show()

sys.exit(app.exec())