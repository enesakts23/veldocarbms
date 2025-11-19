import can
import json
import time
import threading

def fake_can_sender():
    try:
        # Sanal CAN bus oluştur (Linux için)
        bus = can.interface.Bus(channel='vcan0', interface='socketcan')
        print("Fake CAN bus connected on vcan0")

        while True:
            with open('receiveddata.jsonl', 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line.strip())
                        arbitration_id = int(data['id'], 16)
                        msg_data = bytes.fromhex(data['data'])

                        msg = can.Message(arbitration_id=arbitration_id, data=msg_data, is_extended_id=False)
                        bus.send(msg)
                        print(f"Sent: ID={hex(arbitration_id)}, Data={msg_data.hex()}")

                    time.sleep(0.2)  # Her 0.2 saniyede bir mesaj gönder (saniyede 5 mesaj)

    except Exception as e:
        print(f"Fake CAN error: {e}")

if __name__ == "__main__":
    fake_can_sender()