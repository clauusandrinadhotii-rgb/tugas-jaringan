import socket
import threading

# List global untuk menampung semua koneksi aktif
# Ini adalah SHARED RESOURCE
clients = []
clients_lock = threading.Lock() # Gembok pengaman

def broadcast(message, sender_conn):
    """Mengirim pesan ke semua client KECUALI pengirimnya sendiri"""
    # Kita kunci dulu sebelum iterasi agar list tidak berubah di tengah jalan
    with clients_lock:
        for client in clients:
            if client != sender_conn:
                try:
                    client.send(message)
                except:
                    # Jika gagal kirim, anggap putus (akan dibersihkan nanti)
                    client.close()
                    # Menghapus di sini agak tricky saat iterasi, 
                    # jadi biasanya kita skip dulu.
                    pass

def handle_client(conn, addr):
    """Fungsi Tugas untuk setiap Worker Thread"""
    print(f"[NEW CONNECTION] {addr} connected.")

    # Masukkan tamu baru ke buku tamu (dengan aman)
    with clients_lock:
        clients.append(conn)

    try:
        conn.send("Selamat datang di Chat Room!".encode('utf-8'))

        while True:
            # Tunggu pesan (Blocking di thread ini saja, tidak ganggu thread lain)
            message = conn.recv(1024)
            if not message:
                break

            # Format pesan: "[IP]: Isi Pesan"
            msg_decoded = message.decode('utf-8')
            output = f"[{addr[1]}]: {msg_decoded}"
            print(output)

            # Sebarkan pesan
            broadcast(output.encode('utf-8'), conn)

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        # Bersih-bersih saat tamu pulang
        print(f"[DISCONNECT] {addr} keluar.")
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen()
    print("[SERVER STARTED] Menunggu di port 5555...")

    while True:
        # 1. Main Thread standby di sini
        conn, addr = server.accept()

        # 2. Begitu ada tamu, buat Thread baru
        thread = threading.Thread(target=handle_client, args=(conn, addr))

        # 3. Jalankan Thread (Start dan lupakan)
        # Daemon=True artinya thread ini akan mati otomatis jika program utama mati
        thread.daemon = True 
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()