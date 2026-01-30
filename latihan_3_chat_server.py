import socket

# Persiapan Socket (Sama seperti Bab 2)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen(1)
print("=== Chat Server Siap Berjalan ===")

# Menunggu tamu pertama
conn, addr = server.accept()
print(f"[!] Client {addr} bergabung ke dalam sesi chat.")

# INTI CHAT: Loop komunikasi
while True:
    try:
        # 1. Terima Pesan (Akan BLOCKING/diam di sini sampai data masuk)
        data = conn.recv(1024).decode('utf-8')

        # 2. Cek Kondisi Keluar
        # Jika data kosong (koneksi putus) atau user ketik 'bye'
        if not data or data.lower() == 'bye':
            print("[!] Client meminta mengakhiri sesi.")
            break

        print(f"Client > {data}")

        # 3. Kirim Balasan
        reply = input("Server (Anda) > ")
        conn.send(reply.encode('utf-8'))

        # Cek jika Server yang ingin keluar
        if reply.lower() == 'bye':
            print("[!] Anda mengakhiri sesi.")
            break

    except Exception as e:
        print(f"Error Terjadi: {e}")
        break

# Bersih-bersih koneksi
conn.close()
server.close()
print("=== Aplikasi Ditutup ===")