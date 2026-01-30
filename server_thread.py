import socket
import threading

# ===============================
# Fungsi untuk menerima pesan
# ===============================
def receive_messages(conn):
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data or data.lower() == 'bye':
                print("\n[!] Client keluar dari chat.")
                break
            print(f"\nClient > {data}")
        except:
            print("\n[!] Koneksi client terputus.")
            break

# ===============================
# Fungsi untuk mengirim pesan
# ===============================
def send_messages(conn):
    while True:
        try:
            msg = input("Server (Anda) > ")
            conn.send(msg.encode('utf-8'))
            if msg.lower() == 'bye':
                print("[!] Anda mengakhiri chat.")
                break
        except:
            print("[!] Gagal mengirim pesan.")
            break

# ===============================
# Setup Server Socket
# ===============================
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen(1)

print("=== Chat Server Real-Time Siap ===")
conn, addr = server.accept()
print(f"[+] Client {addr} terhubung.")

# ===============================
# Threading
# ===============================
thread_recv = threading.Thread(target=receive_messages, args=(conn,))
thread_send = threading.Thread(target=send_messages, args=(conn,))

thread_recv.start()
thread_send.start()

thread_recv.join()
thread_send.join()

# ===============================
# Cleanup
# ===============================
conn.close()
server.close()
print("=== Server ditutup ===")