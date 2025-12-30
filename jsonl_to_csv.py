import json
import csv
import struct
import math

def parse_temperatures_700(data):
    """0x700 - T1, T2, T3, T4 sıcaklıklarını parse eder"""
    temps = {}
    labels = ["t1", "t2", "t3", "t4"]
    for i in range(4):
        adc = struct.unpack('>H', data[i*2:(i+1)*2])[0]
        volt = (adc / 65535) * 3
        try:
            ntc = volt * 10000 / (3 - volt)
            t_kelvin = 1 / (1 / 298.15 - math.log(10000 / ntc) / 4100)
            t_celsius = t_kelvin - 273.15
            temps[labels[i]] = round(t_celsius, 1)
        except:
            temps[labels[i]] = None
    return temps

def parse_temperatures_701(data):
    """0x701 - T5, T6, TPCB sıcaklıklarını parse eder"""
    temps = {}
    labels = ["t5", "t6", "tpcb"]
    for i in range(3):
        adc = struct.unpack('>H', data[i*2:(i+1)*2])[0]
        volt = (adc / 65535) * 3
        try:
            ntc = volt * 10000 / (3 - volt)
            t_kelvin = 1 / (1 / 298.15 - math.log(10000 / ntc) / 4100)
            t_celsius = t_kelvin - 273.15
            temps[labels[i]] = round(t_celsius, 1)
        except:
            temps[labels[i]] = None
    return temps

def parse_cell_voltages_702(data):
    """0x702 - V1-V8 hücrelerini parse eder"""
    voltages = {}
    for i in range(8):
        v = data[i] * 0.01 + 2
        voltages[f"v{i+1}"] = round(v, 3)
    return voltages

def parse_cell_voltages_703(data):
    """0x703 - V9-V15 hücrelerini parse eder"""
    voltages = {}
    for i in range(7):
        v = data[i] * 0.01 + 2
        voltages[f"v{i+9}"] = round(v, 3)
    return voltages

def parse_pack_status_704(data):
    """0x704 - SOC, SOH, Max Current, Bat Status"""
    soc = data[0]
    soh = data[1]
    max_current = struct.unpack('>H', data[2:4])[0] / 100
    bat_status = data[4]
    return {
        "soc": soc,
        "soh": soh,
        "max_current": round(max_current, 2),
        "bat_status": bat_status
    }

def parse_pack_currents_705(data):
    """0x705 - Current, FET Status"""
    current = struct.unpack('<f', data[0:4])[0]
    fet_status = struct.unpack('>I', data[4:8])[0]
    return {
        "current": round(current, 2),
        "fet_status": fet_status
    }

def parse_errors_706(data):
    """0x706 - Error flags"""
    error_flag_1 = data[0]
    error_flag_2 = data[1]
    return {
        "error_flag_1": error_flag_1,
        "error_flag_2": error_flag_2
    }

def parse_warnings_707(data):
    """0x707 - Delta Cell, OT, OW bitmaps"""
    if len(data) < 8:
        data = data.ljust(8, b'\x00')
    
    delta_raw = struct.unpack('>H', data[0:2])[0]
    delta_cell = delta_raw / 1000.0
    
    ot_raw = data[2]
    ot_active_widgets = [i + 1 for i in range(8) if (ot_raw >> i) & 1]
    
    ow_bitmap_raw = struct.unpack('>H', data[4:6])[0]
    active_ow_cells = [i + 1 for i in range(15) if (ow_bitmap_raw >> i) & 1]
    
    return {
        "delta_cell": round(delta_cell, 3),
        "ot_active": ','.join(map(str, ot_active_widgets)) if ot_active_widgets else '',
        "ow_active": ','.join(map(str, active_ow_cells)) if active_ow_cells else ''
    }

def parse_pack_voltages_708(data):
    """0x708 - Min Cell, Max Cell, Vpack"""
    min_cell = data[0] * 0.01 + 2
    max_cell = data[1] * 0.01 + 2
    vpack = struct.unpack('<H', data[3:5])[0] / 10
    return {
        "min_cell": round(min_cell, 3),
        "max_cell": round(max_cell, 3),
        "vpack": round(vpack, 3)
    }

def decode_error_flag_1(error_flag_1):
    """Error flag 1'i decode eder - string olarak döner"""
    errors = []
    
    flag1_bits = {
        0: "Over Voltage Cell",
        1: "Under Voltage Cell",
        2: "High Temperature Cell",
        3: "Pack Pressure Fault",
        4: "IC Fail",
        5: "Open Wire",
        6: "CAN Error",
        7: "Balance Fault"
    }
    
    for bit, desc in flag1_bits.items():
        if (error_flag_1 >> bit) & 1:
            errors.append(desc)
    
    return ', '.join(errors) if errors else ''

def decode_error_flag_2(error_flag_2):
    """Error flag 2'yi decode eder - string olarak döner"""
    errors = []
    
    flag2_bits = {
        0: "Package Voltage Fault",
        1: "S Channel Delta Fault",
        2: "Temp Open Wire",
        3: "ADC Fault"
    }
    
    for bit, desc in flag2_bits.items():
        if (error_flag_2 >> bit) & 1:
            errors.append(desc)
    
    return ', '.join(errors) if errors else ''


def main():
    input_file = 'receiveddata.jsonl'
    output_file = 'bms_data.csv'
    
    print("Veriler okunuyor ve CSV oluşturuluyor...")
    
    # CSV sütun başlıkları
    headers = [
        'timestamp', 
        # Sıcaklıklar (0x700, 0x701)
        't1', 't2', 't3', 't4', 't5', 't6', 'tpcb',
        # Voltajlar (0x702, 0x703)
        'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v14', 'v15',
        # Pack Status (0x704)
        'soc', 'soh', 'max_current',
        # Pack Currents (0x705)
        'current',
        # Errors (0x706) - string olarak
        'error_flag_1', 'error_flag_2',
        # Warnings (0x707)
        'ot_active',
        # Pack Voltages (0x708)
        'min_cell', 'max_cell', 'vpack'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        # Her timestamp için toplanan veriler
        current_timestamp = None
        row_data = {}
        total_rows = 0
        
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    record = json.loads(line.strip())
                    timestamp = record['timestamp']
                    can_id = int(record['id'], 16)
                    data = bytes.fromhex(record['data'])
                    
                    # Yeni timestamp geldiğinde önceki satırı yaz
                    if current_timestamp is not None and timestamp != current_timestamp:
                        # Satırı oluştur ve yaz
                        row = [current_timestamp]
                        
                        # Sıcaklıklar
                        row.extend([
                            row_data.get('t1', ''),
                            row_data.get('t2', ''),
                            row_data.get('t3', ''),
                            row_data.get('t4', ''),
                            row_data.get('t5', ''),
                            row_data.get('t6', ''),
                            row_data.get('tpcb', '')
                        ])
                        
                        # Voltajlar
                        row.extend([
                            row_data.get('v1', ''),
                            row_data.get('v2', ''),
                            row_data.get('v3', ''),
                            row_data.get('v4', ''),
                            row_data.get('v5', ''),
                            row_data.get('v6', ''),
                            row_data.get('v7', ''),
                            row_data.get('v8', ''),
                            row_data.get('v9', ''),
                            row_data.get('v10', ''),
                            row_data.get('v11', ''),
                            row_data.get('v12', ''),
                            row_data.get('v13', ''),
                            row_data.get('v14', ''),
                            row_data.get('v15', '')
                        ])
                        
                        # Pack Status
                        row.extend([
                            row_data.get('soc', ''),
                            row_data.get('soh', ''),
                            row_data.get('max_current', '')
                        ])
                        
                        # Pack Currents
                        row.extend([
                            row_data.get('current', '')
                        ])
                        
                        # Errors - string olarak decode edilmiş
                        row.extend([
                            row_data.get('error_flag_1', ''),
                            row_data.get('error_flag_2', '')
                        ])
                        
                        # Warnings
                        row.extend([
                            row_data.get('ot_active', '')
                        ])
                        
                        # Pack Voltages
                        row.extend([
                            row_data.get('min_cell', ''),
                            row_data.get('max_cell', ''),
                            row_data.get('vpack', '')
                        ])
                        
                        writer.writerow(row)
                        total_rows += 1
                        
                        # Yeni satır için sıfırla
                        row_data = {}
                    
                    current_timestamp = timestamp
                    
                    # CAN ID'ye göre parse et ve row_data'ya ekle
                    if can_id == 0x700:
                        temps = parse_temperatures_700(data)
                        row_data.update(temps)
                    elif can_id == 0x701:
                        temps = parse_temperatures_701(data)
                        row_data.update(temps)
                    elif can_id == 0x702:
                        volts = parse_cell_voltages_702(data)
                        row_data.update(volts)
                    elif can_id == 0x703:
                        volts = parse_cell_voltages_703(data)
                        row_data.update(volts)
                    elif can_id == 0x704:
                        pack = parse_pack_status_704(data)
                        # bat_status'u ekleme
                        row_data['soc'] = pack.get('soc', '')
                        row_data['soh'] = pack.get('soh', '')
                        row_data['max_current'] = pack.get('max_current', '')
                    elif can_id == 0x705:
                        curr = parse_pack_currents_705(data)
                        # fet_status'u ekleme, sadece current
                        row_data['current'] = curr.get('current', '')
                    elif can_id == 0x706:
                        errs = parse_errors_706(data)
                        # Error flag'leri string'e çevir
                        row_data['error_flag_1'] = decode_error_flag_1(errs['error_flag_1'])
                        row_data['error_flag_2'] = decode_error_flag_2(errs['error_flag_2'])
                    elif can_id == 0x707:
                        warns = parse_warnings_707(data)
                        # delta_cell ve ow_active'i ekleme, sadece ot_active
                        row_data['ot_active'] = warns.get('ot_active', '')
                    elif can_id == 0x708:
                        pack_v = parse_pack_voltages_708(data)
                        row_data.update(pack_v)
                    
                    # İlerleme göster
                    if line_num % 5000 == 0:
                        print(f"{line_num} satır işlendi, {total_rows} CSV satırı yazıldı...")
                        
                except json.JSONDecodeError as e:
                    print(f"Satır {line_num} JSON parse hatası: {e}")
                    continue
                except Exception as e:
                    print(f"Satır {line_num} işleme hatası: {e}")
                    continue
            
            # Son satırı yaz
            if current_timestamp is not None and row_data:
                row = [current_timestamp]
                
                # Sıcaklıklar
                row.extend([
                    row_data.get('t1', ''),
                    row_data.get('t2', ''),
                    row_data.get('t3', ''),
                    row_data.get('t4', ''),
                    row_data.get('t5', ''),
                    row_data.get('t6', ''),
                    row_data.get('tpcb', '')
                ])
                
                # Voltajlar
                row.extend([
                    row_data.get('v1', ''),
                    row_data.get('v2', ''),
                    row_data.get('v3', ''),
                    row_data.get('v4', ''),
                    row_data.get('v5', ''),
                    row_data.get('v6', ''),
                    row_data.get('v7', ''),
                    row_data.get('v8', ''),
                    row_data.get('v9', ''),
                    row_data.get('v10', ''),
                    row_data.get('v11', ''),
                    row_data.get('v12', ''),
                    row_data.get('v13', ''),
                    row_data.get('v14', ''),
                    row_data.get('v15', '')
                ])
                
                # Pack Status
                row.extend([
                    row_data.get('soc', ''),
                    row_data.get('soh', ''),
                    row_data.get('max_current', '')
                ])
                
                # Pack Currents
                row.extend([
                    row_data.get('current', '')
                ])
                
                # Errors - string olarak decode edilmiş
                row.extend([
                    row_data.get('error_flag_1', ''),
                    row_data.get('error_flag_2', '')
                ])
                
                # Warnings
                row.extend([
                    row_data.get('ot_active', '')
                ])
                
                # Pack Voltages
                row.extend([
                    row_data.get('min_cell', ''),
                    row_data.get('max_cell', ''),
                    row_data.get('vpack', '')
                ])
                
                writer.writerow(row)
                total_rows += 1
    
    print(f"\nCSV dosyası oluşturuldu: {output_file}")
    print(f"Toplam {total_rows} satır yazıldı")

if __name__ == '__main__':
    main()
