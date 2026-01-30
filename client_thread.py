import socket
import threading

# ===============================
# Fungsi terima pesan
# ===============================
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data or data.lower() == 'bye':
                print("\n[!] Server keluar dari chat.")
                break
            print(f"\nServer > {data}")
        except:
            print("\n[!] Koneksi ke server terputus.")
            break

# ===============================
# Fungsi kirim pesan
# ===============================
def send_messages(sock):
    while True:
        try:
            msg = input("Client (Anda) > ")
            sock.send(msg.encode('utf-8'))
            if msg.lower() == 'bye':
                print("[!] Anda keluar dari chat.")
                break
        except:
            print("[!] Gagal mengirim pesan.")
            break

# ===============================
# Setup Client Socket
# ===============================
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5000))
print("=== Terhubung ke Chat Server ===")

# ===============================
# Threading
# ===============================
thread_recv = threading.Thread(target=receive_messages, args=(client,))
thread_send = threading.Thread(target=send_messages, args=(client,))

thread_recv.start()
thread_send.start()

thread_recv.join()
thread_send.join()

# ===============================
# Cleanup
# ===============================
client.close()
print("=== Client ditutup ===")