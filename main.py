import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel, QStackedWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
import voltage
import temperature
import packview
import configuration
import can
import threading
import json
import time
import struct

import struct

def parse_pack_status(data):
    soc = data[0]
    soh = data[1]
    state_code = data[7]
    states = {0: "IDLE", 1: "CHARGE", 2: "DISCHARGE"}
    state = states.get(state_code, f"UNKNOWN({state_code})")
    return {"SOC": f"{soc}%", "SOH": f"{soh}%", "State": state}

def parse_pack_voltages(data):
    min_cell = struct.unpack('>H', data[0:2])[0] / 1000
    max_cell = struct.unpack('>H', data[2:4])[0] / 1000
    delta = struct.unpack('>H', data[4:6])[0] / 1000
    total = struct.unpack('>H', data[6:8])[0] / 1000
    return {"Min_Cell_Voltage": f"{min_cell:.3f} V", "Max_Cell_Voltage": f"{max_cell:.3f} V", "Cell_Voltage_Delta": f"{delta:.3f} V", "Total_Pack_Voltage": f"{total:.3f} V"}

def parse_pack_currents(data):
    current = struct.unpack('>i', data[0:4])[0] / 100  # /100 for A
    charging_fet = data[4]
    discharging_fet = data[5]
    return {"Current": f"{current:.2f} A", "Charging_FET_Status": charging_fet, "Discharging_FET_Status": discharging_fet}

def parse_overall_temperatures(data):
    min_temp = struct.unpack('>H', data[0:2])[0] * 0.1
    max_temp = struct.unpack('>H', data[2:4])[0] * 0.1
    delta = struct.unpack('>H', data[4:6])[0] * 0.1
    mean_temp = struct.unpack('>H', data[6:8])[0] * 0.1
    return {"Min_Temp": f"{min_temp:.1f} °C", "Max_Temp": f"{max_temp:.1f} °C", "Temp_Delta": f"{delta:.1f} °C", "Mean_Temp": f"{mean_temp:.1f} °C"}

def parse_cell_voltages_1(data):
    voltages = {}
    for i in range(8):
        v = data[i] * 10 / 1000
        voltages[f"Cell_Voltage_{i+1}"] = f"{v:.3f} V"
    return voltages

def parse_cell_voltages_2(data):
    voltages = {}
    for i in range(8):
        v = data[i] * 10 / 1000
        voltages[f"Cell_Voltage_{i+9}"] = f"{v:.3f} V"
    return voltages

def parse_module_temperatures_1(data):
    temps = {}
    for i in range(4):
        t = struct.unpack('>H', data[i*2:(i+1)*2])[0] * 0.1
        temps[f"Module_Temp_{i+1}"] = f"{t:.1f} °C"
    return temps

def parse_module_temperatures_2(data):
    temps = {}
    for i in range(4):
        t = struct.unpack('>H', data[i*2:(i+1)*2])[0] * 0.1
        temps[f"Module_Temp_{i+5}"] = f"{t:.1f} °C"
    return temps

parsers = {
    0x02: ("PACK_STATUS", parse_pack_status),
    0x03: ("PACK_VOLTAGES", parse_pack_voltages),
    0x04: ("PACK_CURRENTS", parse_pack_currents),
    0x06: ("OVERALL_TEMPERATURES", parse_overall_temperatures),
    0x08: ("CELL_VOLTAGES_1", parse_cell_voltages_1),
    0x09: ("CELL_VOLTAGES_2", parse_cell_voltages_2),
    0x40: ("MODULE_TEMPERATURES_1", parse_module_temperatures_1),
    0x41: ("MODULE_TEMPERATURES_2", parse_module_temperatures_2),
}

def can_listener():
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=250000)
        print("CAN bus connected on can0 with bitrate 250000")
        with open('receiveddata.jsonl', 'a') as f:
            while True:
                msg = bus.recv()
                if msg:
                    # Konsola yaz
                    print(f"Received: ID={msg.arbitration_id:X}, Data={msg.data.hex()}, DLC={msg.dlc}")
                    parsed = None
                    if msg.arbitration_id in parsers:
                        name, parser = parsers[msg.arbitration_id]
                        try:
                            parsed = parser(msg.data)
                            print(f"Parsed {name}: {parsed}")
                        except Exception as e:
                            print(f"Parse error for {name}: {e}")
                    # JSONL'ye yaz
                    data = {
                        "timestamp": time.time(),
                        "id": msg.arbitration_id,
                        "data": msg.data.hex(),
                        "dlc": msg.dlc,
                        "parsed": parsed
                    }
                    f.write(json.dumps(data) + '\n')
                    f.flush()
    except Exception as e:
        print(f"CAN error: {e}")

# CAN thread'ini başlat
can_thread = threading.Thread(target=can_listener, daemon=True)
can_thread.start()

app = QApplication(sys.argv)
current_page = "Voltage"  # default olarak voltage sayfası açılacak main.py başlatılıdığı zmaanç.

def update_button_styles():
    # Common colors
    accent = "#00b51a"

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
        background-color: rgba(0,181,26,0.08);
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

window = QWidget()
window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
window.setGeometry(100, 100, 1000, 540)

header = QWidget()
header.setStyleSheet("background-color: #000000;")
header.setFixedHeight(50)
header_layout = QHBoxLayout()
header_layout.setContentsMargins(0, 0, 0, 0)
header_layout.setSpacing(0)

# Logo
logo_label = QLabel()
pixmap = QPixmap("veldologo.png")
scaled_pixmap = pixmap.scaledToHeight(50, Qt.TransformationMode.SmoothTransformation)
logo_label.setPixmap(scaled_pixmap)
logo_label.setFixedSize(100, 50)
logo_label.setStyleSheet("background: transparent;")
header_layout.addWidget(logo_label)
# Spacer ekle
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