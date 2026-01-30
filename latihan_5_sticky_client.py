# latihan_5_sticky_client.py
import socket
import time

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5555))

    print("=== Uji Coba Sticky Packet ===")
    print("Mengirim 10 pesan secepat kilat...")

    # Payload pesan diakhiri \n sebagai delimiter
    pesan = "HaloServer\n"

    # Kirim 10x berturut-turut tanpa jeda
    # Tanpa framing di server, ini pasti akan diterima sebagai satu blob raksasa
    for i in range(10):
        data = f"PesanKe-{i+1}|{pesan}"
        client.send(data.encode('utf-8'))

    print("Selesai mengirim. Cek terminal Server!")
    client.close()

if __name__ == "__main__":
    run_client()