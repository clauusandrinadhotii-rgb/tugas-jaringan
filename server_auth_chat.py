import socket

PASSWORD = "12345"   # password sederhana

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen(1)

print("=== Chat Server dengan Autentikasi ===")

conn, addr = server.accept()
print(f"[+] Client {addr} terhubung")

# ==========================
# AUTHENTIKASI
# ==========================
conn.send("Password: ".encode('utf-8'))
password = conn.recv(1024).decode('utf-8')

if password != PASSWORD:
    conn.send("Password salah! Koneksi ditutup.".encode('utf-8'))
    conn.close()
    print("[!] Client gagal autentikasi")
else:
    conn.send("Password benar. Selamat datang di chat.\n".encode('utf-8'))
    print("[+] Client berhasil login")

    # ==========================
    # CHAT LOOP
    # ==========================
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')

            if not data or data.lower() == 'bye':
                print("[!] Client keluar.")
                break

            print(f"Client > {data}")

            reply = input("Server > ")
            conn.send(reply.encode('utf-8'))

            if reply.lower() == 'bye':
                print("[!] Server keluar.")
                break

        except Exception as e:
            print("Error:", e)
            break

conn.close()
server.close()
print("=== Server ditutup ===")