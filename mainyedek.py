import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel, QStackedWidget
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, QTimer
import voltage
import temperature
import packview
import configuration
import can
import threading
import json
import time
from datetime import datetime
import struct
import math
import platform
import subprocess

# can den gelen dataalrı diğer sayfalarda kullanabilmek için global değişkenler oluşturdum.
voltage_data = {}
temperature_data = {}
pack_data = {}

def parse_pack_status_704(data):
    global pack_data
    soc = data[0]
    soh = data[1]
    max_current = struct.unpack('>H', data[2:4])[0] / 100  # /100 for A
    bat_status = data[4]
    parsed = {"SOC": f"{soc}%", "SOH": f"{soh}%", "Max_Current": f"{max_current:.2f} A", "Bat_Status": bat_status}
    pack_data.update(parsed)
    return parsed

def parse_pack_currents_705(data):
    global pack_data
    current = struct.unpack('>i', data[0:4])[0] / 100  # /100 for A
    fet_status = struct.unpack('>I', data[4:8])[0]
    parsed = {"Current": f"{current:.2f} A", "FET_Status": fet_status}
    pack_data.update(parsed)
    return parsed

def parse_errors_706(data):
    global pack_data
    error_flag_1 = data[0]
    error_flag_2 = data[1]
    combined_error_flags = (error_flag_2 << 8) | error_flag_1
    
    # Bit definitions for errors
    error_bits = {
        0: "Over Voltage Cell",
        1: "Under Voltage Cell",
        2: "High temperature Cell",
        3: "Pack Pressure Fault",
        4: "Ic fail",
        5: "Open Wire",
        6: "Can Error",
        7: "Packet Loss",
        8: "Package Voltage Fault",
        9: "S channel delta fault",
        10: "Temp Open wire",
        11: "ADC fault",
        12: "Balance Fault",
        13: "Empty",
        14: "Empty",
        15: "Empty"
    }
    
    active_errors = []
    for bit in range(16):
        if combined_error_flags & (1 << bit):
            active_errors.append(error_bits.get(bit, f"Unknown Bit {bit}"))
    
    # OV Cell
    ov_flags = struct.unpack('>H', data[2:4])[0]
    active_ov_cells = [bit + 1 for bit in range(16) if ov_flags & (1 << bit)]
    
    # UV Cell
    uv_flags = struct.unpack('>H', data[4:6])[0]
    active_uv_cells = [bit + 1 for bit in range(16) if uv_flags & (1 << bit)]
    
    # OW Cell
    ow_flags = struct.unpack('>H', data[6:8])[0]
    active_ow_cells = [bit + 1 for bit in range(16) if ow_flags & (1 << bit)]
    
    parsed = {"Combined_Error_Flags": combined_error_flags, "Active_Errors": active_errors, "Active_OV_Cells": active_ov_cells, "Active_UV_Cells": active_uv_cells, "Active_OW_Cells": active_ow_cells}
    pack_data.update(parsed)
    return parsed

def parse_warnings_707(data):
    global pack_data
    delta_cell = struct.unpack('>H', data[0:2])[0] / 1000
    ot_cell = struct.unpack('>H', data[2:4])[0]  # 16-bit
    ow_temp_cell = struct.unpack('>H', data[4:6])[0] * 0.1
    parsed = {"Delta_Cell": f"{delta_cell:.3f} V", "OT_Cell": ot_cell, "OW_Temp_Cell": f"{ow_temp_cell:.1f} °C"}
    pack_data.update(parsed)
    return parsed

def parse_pack_voltages_708(data):
    global pack_data
    min_cell = data[0] * 0.01 + 2
    max_cell = data[1] * 0.01 + 2
    max_cell_delta = data[2] * 0.01
    vpack = struct.unpack('<H', data[3:5])[0] / 10
    parsed = {"Min_Cell": f"{min_cell:.3f} V", "Max_Cell": f"{max_cell:.3f} V", "Max_Cell_Delta": f"{max_cell_delta:.3f} V", "Vpack": f"{vpack:.3f} V"}
    pack_data.update(parsed)
    return parsed

def parse_cell_voltages_702(data):
    global voltage_data
    voltages = {}
    for i in range(8):
        v = data[i] * 0.01 + 2
        voltages[f"V{i+1}"] = f"{v:.3f} V"
    voltage_data.update(voltages)
    return voltages

def parse_cell_voltages_703(data):
    global voltage_data
    voltages = {}
    for i in range(7):
        v = data[i] * 0.01 + 2
        voltages[f"V{i+9}"] = f"{v:.3f} V"
    voltage_data.update(voltages)
    return voltages

def parse_temperatures_700(data):
    global temperature_data
    temps = {}
    labels = ["T1", "T2", "T3", "T4"]
    for i in range(4):
        adc = struct.unpack('>H', data[i*2:(i+1)*2])[0]
        volt = (adc / 65535) * 3
        ntc = volt * 10000 / (3 - volt)
        t_kelvin = 1 / (1 / 298.15 - math.log(10000 / ntc) / 4100)
        t_celsius = t_kelvin - 273.15
        temps[labels[i]] = f"{t_celsius:.1f} °C"
    temperature_data.update(temps)
    return temps

def parse_temperatures_701(data):
    global temperature_data
    temps = {}
    labels = ["T5", "T6", "TPCB"] 
    for i in range(3): 
        adc = struct.unpack('>H', data[i*2:(i+1)*2])[0]
        volt = (adc / 65535) * 3
        ntc = volt * 10000 / (3 - volt)
        t_kelvin = 1 / (1 / 298.15 - math.log(10000 / ntc) / 4100)
        t_celsius = t_kelvin - 273.15
        temps[labels[i]] = f"{t_celsius:.1f} °C"
    temperature_data.update(temps)
    return temps

parsers = {
    0x704: ("PACK_STATUS_704", parse_pack_status_704),
    0x705: ("PACK_CURRENTS_705", parse_pack_currents_705),
    0x706: ("ERRORS_706", parse_errors_706),
    0x707: ("WARNINGS_707", parse_warnings_707),
    0x708: ("PACK_VOLTAGES_708", parse_pack_voltages_708),
    0x702: ("CELL_VOLTAGES_702", parse_cell_voltages_702),
    0x703: ("CELL_VOLTAGES_703", parse_cell_voltages_703),
    0x700: ("TEMPERATURES_700", parse_temperatures_700),
    0x701: ("TEMPERATURES_701", parse_temperatures_701),
}

def can_listener():
    try:
        if platform.system() == 'Linux':
            bus = can.interface.Bus(channel='can0', interface='socketcan', bitrate=500000)
            print("CAN bus connected on can0 with bitrate 500000 (Linux socketcan)")
        elif platform.system() == 'Windows':
            bus = can.interface.Bus(channel=(0, 1), interface='canalystii', bitrate=500000)
            print("CAN bus connected on CANalyst-II channels 0 and 1 with bitrate 500000 (Windows)")
        else:
            print("Unsupported platform for CAN bus")
            return
        with open('receiveddata.jsonl', 'a') as f:
            while True:
                msg = bus.recv()
                if msg:
                    parsed = None
                    if msg.arbitration_id in parsers:
                        name, parser = parsers[msg.arbitration_id]
                        try:
                            parsed = parser(msg.data)
                        except Exception as e:
                            print(f"Parse error for {name}: {e}")

                    data = {  # Gelen CAN B dataalrını hex oalrak timestampt , can id  , ham (hext) datayı receiveddata.jsonl dosyası oluşturup içine yazıyorum. Dosya var ise alt satıra eklemeye deva mediyor.
                        "timestamp": datetime.fromtimestamp(time.time()).strftime('%d/%m/%Y %H:%M:%S'),
                        "id": hex(msg.arbitration_id),
                        "data": msg.data.hex()
                    }
                    f.write(json.dumps(data) + '\n')
                    f.flush()
    except Exception as e:
        print(f"CAN error: {e}")

# CAN thread'ini başlat
if platform.system() == 'Linux':
    try:
        subprocess.run(['sudo', 'ip', 'link', 'set', 'can0', 'down'], check=True)
        subprocess.run(['sudo', 'ip', 'link', 'set', 'can0', 'up', 'type', 'can', 'bitrate', '500000'], check=True)
        print("Executed: sudo ip link set can0 down and up")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute CAN interface commands: {e}")

can_thread = threading.Thread(target=can_listener, daemon=True)
can_thread.start()

app = QApplication(sys.argv)
current_page = "Voltage"  # default olarak voltage sayfası açılacak main.py başlatılıdığı zmaanç.

def update_button_styles():

    accent = "#0077A8"
    normal = f"""
    QPushButton {{
        background-color: transparent;
        color: #ffffff;
        border: 2px solid {accent};
        border-radius: 8px;
        padding: 0 20px;
    }}
    QPushButton:hover {{
        background-color: rgba(0,119,168,0.08);
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

# Timer to update displays
timer = QTimer()
timer.timeout.connect(lambda: (voltage.update_voltage_display(), temperature.update_temperature_display(), packview.update_pack_display()))
timer.start(1000)  # Update every 1 second

sys.exit(app.exec())