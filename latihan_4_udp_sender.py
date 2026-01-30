# latihan_4_udp_sender.py
import socket
import time
import random

# PENTING: Gunakan SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Alamat Server Pusat
TARGET_IP = 'localhost' # Ganti IP ini jika server ada di komputer lain
TARGET_PORT = 9999
TARGET_ADDR = (TARGET_IP, TARGET_PORT)

print(f"=== Sensor Aktif. Mengirim data ke {TARGET_ADDR} ===")

try:
    while True:
        # Simulasi pembacaan suhu (20-35 derajat Celcius)
        suhu = random.randint(20, 35)
        kelembaban = random.randint(40, 90)

        # Format data: CSV sederhana atau JSON string
        payload = f"TEMP:{suhu}C|HUM:{kelembaban}%"

        # Kirim Paket (Fire!)
        # Perhatikan kita harus menyertakan TARGET_ADDR di setiap pengiriman
        sock.sendto(payload.encode('utf-8'), TARGET_ADDR)

        print(f"Mengirim -> {payload}")

        # Sensor tidur sejenak untuk hemat baterai
        time.sleep(1) 

except KeyboardInterrupt:
    print("\nSensor dimatikan.")
    sock.close()