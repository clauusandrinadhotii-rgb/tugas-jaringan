import socket

# 1. Membuat Soket (Domain: IPv4, Tipe: TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Binding (Mengikat ke alamat localhost port 12345)
# localhost artinya server hanya bisa diakses dari komputer ini saja (aman untuk latihan)
server_socket.bind(('localhost', 12345))

# 3. Listening (Mempersiapkan antrian, max 1 antrian)
server_socket.listen(1)
print("Server: Saya siap dan sedang menunggu tamu di port 12345...")

# 4. Accepting (BLOCKING CALL)
# Program akan BERHENTI di sini sampai ada Client yang connect.
conn, addr = server_socket.accept()
print(f"Server: Tamu datang dari alamat {addr}")

# 5. Komunikasi Data
# Terima data mentah (bytes), lalu decode ke string
msg = conn.recv(1024).decode('utf-8')
print(f"Server: Tamu berkata '{msg}'")

# Kirim balasan (jangan lupa encode ke bytes)
conn.send("Halo Tamu, salam kenal!".encode('utf-8'))

# 6. Menutup Koneksi
conn.close()
print("Server: Sesi selesai.")