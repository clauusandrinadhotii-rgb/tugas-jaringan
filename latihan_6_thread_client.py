import socket
import threading

def receive_messages(sock):
    """Thread penerima pesan"""
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                print("\n[!] Server memutus koneksi.")
                break
            print(f"\n{data}")
        except:
            print("\n[!] Koneksi ke server terputus.")
            break

def send_messages(sock):
    """Thread pengirim pesan"""
    while True:
        try:
            msg = input("You > ")
            sock.send(msg.encode('utf-8'))

            if msg.lower() == 'bye':
                print("[!] Keluar dari chat.")
                break
        except:
            print("[!] Gagal mengirim pesan.")
            break

# ==========================
# Setup Socket Client
# ==========================
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

print("=== Terhubung ke Server Chat (Threading) ===")
print("Ketik pesan untuk mengirim")
print("Ketik 'bye' untuk keluar\n")

# ==========================
# Threading
# ==========================
thread_recv = threading.Thread(target=receive_messages, args=(client,))
thread_send = threading.Thread(target=send_messages, args=(client,))

thread_recv.daemon = True
thread_send.daemon = True

thread_recv.start()
thread_send.start()

# ==========================
# Menjaga program tetap hidup
# ==========================
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\n[!] Client dihentikan.")
finally:
    client.close()