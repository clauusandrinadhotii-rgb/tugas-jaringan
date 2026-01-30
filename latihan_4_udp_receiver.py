# latihan_4_udp_receiver.py
import socket

# 1. Gunakan SOCK_DGRAM untuk UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Bind ke IP/Port tertentu (Agar paket tahu mau masuk lewat pintu mana)
# 0.0.0.0 berarti menerima dari semua IP (bukan cuma localhost)
sock.bind(('0.0.0.0', 9999))

print("=== UDP Monitoring Server Berjalan ===")
print("Menunggu data sensor...")

while True:
    # 3. recvfrom: Menerima paket DARI SIAPA SAJA
    # Return value: (bytes_data, (ip_pengirim, port_pengirim))
    data, addr = sock.recvfrom(1024)

    # Decoding dan Display
    pesan = data.decode('utf-8')
    print(f"[Sensor {addr}] Melaporkan: {pesan}")