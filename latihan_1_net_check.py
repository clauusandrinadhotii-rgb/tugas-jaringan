import socket

def check_net_info():
    print("=== Network Information Tool ===")
    try:
        # 1. Mengambil Hostname (Nama Komputer)
        # Bermanfaat untuk log file agar tahu server mana yang memproses request
        hostname = socket.gethostname()

        # 2. Mengambil IP Address Lokal
        # Fungsi ini melakukan resolusi DNS lokal
        ip_address = socket.gethostbyname(hostname)

        print(f"Hostname  : {hostname}")
        print(f"IP Address: {ip_address}")

    except socket.error as e:
        # Best Practice: Selalu tangani potensi error jaringan
        print(f"Gagal mengambil informasi jaringan: {e}")

if __name__ == "__main__":
    check_net_info()