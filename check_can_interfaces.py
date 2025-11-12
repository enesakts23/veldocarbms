import can

# Mevcut CAN interface'lerini listele
configs = can.interface.detect_available_configs()
print("Mevcut CAN interface'leri:")
for config in configs:
    print(f"Interface: {config['interface']}, Channel: {config['channel']}, Bitrate: {config.get('bitrate', 'N/A')}")

# PCAN için özel olarak
try:
    import can.interfaces.pcan
    devices = can.interfaces.pcan.PcanBus.list_devices()
    print("\nPCAN cihazları:")
    for device in devices:
        print(device)
except ImportError:
    print("PCAN backend yüklü değil.")
except Exception as e:
    print(f"PCAN cihaz listesi alınamadı: {e}")