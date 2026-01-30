import socket

# 1. Membuat Soket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connect (Mengetuk pintu server)
# Pastikan IP dan Port SAMA PERSIS dengan server
print("Client: Mencoba menghubungi server...")
client_socket.connect(('localhost', 12345))

# 3. Kirim Pesan
pesan = "Halo Server! Ini percobaan pertama saya."
client_socket.send(pesan.encode('utf-8')) # Encode string ke bytes

# 4. Terima Balasan
response = client_socket.recv(1024).decode('utf-8') # Decode bytes ke string
print(f"Client: Mendapat balasan '{response}'")

# 5. Tutup
client_socket.close()