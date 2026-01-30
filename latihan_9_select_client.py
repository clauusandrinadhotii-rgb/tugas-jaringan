import socket
import select
import sys

def run_chat_client():
    server_ip = '127.0.0.1'
    server_port = 9000

    # Buat socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    client_socket.setblocking(False)

    print("=== Terhubung ke Select Chat Server ===")
    print("Ketik pesan lalu ENTER")
    print("Ketik 'bye' untuk keluar\n")

    # Socket yang dipantau:
    # 1. client_socket -> data dari server
    # 2. sys.stdin     -> input dari keyboard
    socket_list = [sys.stdin, client_socket]

    while True:
        # Pantau input keyboard & socket server
        read_sockets, _, _ = select.select(socket_list, [], [])

        for sock in read_sockets:

            # =====================
            # DATA DARI SERVER
            # =====================
            if sock == client_socket:
                data = sock.recv(1024)
                if not data:
                    print("\n[!] Server menutup koneksi.")
                    sys.exit()
                else:
                    print(data.decode().strip())

            # =====================
            # INPUT USER
            # =====================
            else:
                msg = sys.stdin.readline()
                if msg.strip().lower() == 'bye':
                    client_socket.send(msg.encode())
                    print("[!] Keluar dari chat.")
                    sys.exit()
                else:
                    client_socket.send(msg.encode())

if __name__ == "__main__":
    try:
        run_chat_client()
    except KeyboardInterrupt:
        print("\nClient dihentikan.")