# VELDO CAR BMS# VELDO CAR BMS



Bu proje, elektrikli araç batarya yönetim sistemi (BMS) için CAN mesajlarını dinler ve parse eder.Bu proje, elektrikli araç batarya yönetim sistemi (BMS) için CAN mesajlarını dinler ve parse eder.



## 🔋 CAN Mesaj Tablosu## 🔋 CAN Mesaj Yapısı



| CAN ID | Mesaj Adı | İçerik | Dönüşüm | Örnek |### 0x02 - PACK_STATUS

|--------|-----------|--------|---------|-------|- **İçerik**: SOC (Byte 0), SOH (Byte 1), State (Byte 7)

| 0x02 | PACK_STATUS | SOC (Byte0), SOH (Byte1), State (Byte7) | SOC/SOH: Raw %, State: 0=IDLE,1=CHARGE,2=DISCHARGE | SOC:64%, SOH:64%, State:DISCHARGE |- **Dönüşüm**: SOC ve SOH doğrudan %, State: 0=IDLE, 1=CHARGE, 2=DISCHARGE

| 0x03 | PACK_VOLTAGES | Min/Max/Delta Cell V (Bytes 0-5), Total V (6-7) | V = Raw / 1000 | Total: 51.2 V |- **Örnek Veri**: `64 64 00 00 00 00 00 02` → SOC: 100%, SOH: 100%, State: DISCHARGE

| 0x04 | PACK_CURRENTS | Current (Bytes 0-3), FET Status (4-5) | I = Raw / 100 A | Current: 100 A |

| 0x06 | OVERALL_TEMPERATURES | Min/Max/Delta/Mean Temp (Bytes 0-7) | T = Raw × 0.1 °C | Min:20.0°C, Max:30.0°C |### 0x03 - PACK_VOLTAGES

| 0x08 | CELL_VOLTAGES_1 | Cell 1-8 Voltages (1 byte each) | V = Byte × 10 / 1000 | Cell1: 2.5 V |- **İçerik**: Min_Cell_Voltage (Bytes 0-1), Max_Cell_Voltage (2-3), Cell_Voltage_Delta (4-5), Total_Pack_Voltage (6-7)

| 0x09 | CELL_VOLTAGES_2 | Cell 9-16 Voltages (1 byte each) | V = Byte × 10 / 1000 | Cell9: 2.5 V |- **Dönüşüm**: V = Raw / 1000 (V)

| 0x40 | MODULE_TEMPERATURES_1 | Module 1-4 Temps (2 bytes each) | T = Raw × 0.1 °C | Modül1: 20.0°C |- **Örnek Veri**: `0A F0 13 88 00 00 C8 00` → Total: 51.2 V

| 0x41 | MODULE_TEMPERATURES_2 | Module 5-8 Temps (2 bytes each) | T = Raw × 0.1 °C | Modül5: 20.0°C |

### 0x04 - PACK_CURRENTS

## 📘 Teknik Notlar- **İçerik**: Current (Bytes 0-3), Charging_FET_Status (Byte 4), Discharging_FET_Status (Byte 5)

- Tüm mesajlar 8 byte.- **Dönüşüm**: I = Raw / 100 (A)

- Byte order: Big-endian.- **Örnek Veri**: `00 00 27 10 03 00 00 00` → Current: 100 A

- Voltajlar mV raw, akımlar mA raw, sıcaklıklar 0.1°C raw.
### 0x06 - OVERALL_TEMPERATURES
- **İçerik**: Min_Temp (0-1), Max_Temp (2-3), Temp_Delta (4-5), Mean_Temp (6-7)
- **Dönüşüm**: T = Raw × 0.1 (°C)
- **Örnek Veri**: `00 C8 01 2C 00 1E 01 00` → Min: 20.0°C, Max: 30.0°C

### 0x08 - CELL_VOLTAGES_1 (Hücre 1-8)
- **İçerik**: Her byte bir hücre voltajı
- **Dönüşüm**: V = Byte × 10 / 1000 (V)
- **Örnek Veri**: `FA FB FC FD FE FF F0 F1` → Hücre1: 2.5 V, Hücre2: 2.51 V, ...

### 0x09 - CELL_VOLTAGES_2 (Hücre 9-16)
- **İçerik**: Her byte bir hücre voltajı
- **Dönüşüm**: V = Byte × 10 / 1000 (V)
- **Örnek Veri**: `FA FB FC FD FE FF F0 F1` → Hücre9: 2.5 V, ...

### 0x40 - MODULE_TEMPERATURES_1 (Modül 1-4)
- **İçerik**: Her 2 byte bir modül sıcaklığı
- **Dönüşüm**: T = Raw × 0.1 (°C)
- **Örnek Veri**: `00 C8 00 C9 00 D0 00 D2` → Modül1: 20.0°C, Modül2: 20.1°C, ...

### 0x41 - MODULE_TEMPERATURES_2 (Modül 5-8)
- **İçerik**: Her 2 byte bir modül sıcaklığı
- **Dönüşüm**: T = Raw × 0.1 (°C)
- **Örnek Veri**: `00 C8 00 C9 00 D0 00 D2` → Modül5: 20.0°C, ...

## � Teknik Notlar
- Tüm mesajlar 8 byte'dır.
- Voltajlar mV cinsinden, akımlar mA cinsinden raw değerler taşır.
- Sıcaklıklar 0.1°C çözünürlükte.
- Byte order: Big-endian (MSB first).
