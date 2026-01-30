import socket
import select
import sys

def run_chat_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 9000))
    server_socket.listen(10)

    # List untuk menampung semua socket yang sedang dipantau oleh 'Satpam'
    socket_list = [server_socket]

    # Dictionary opsional untuk menyimpan nama user (jika mau)
    clients = {} 

    print(f"=== Select Server (Single Thread) berjalan di port 9000 ===")

    while True:
        # Panggilan ke OS: "Tolong pantau socket_list ini"
        # Fungsi ini akan BLOCKING sampai minimal ada satu socket yang aktif
        read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

        for sock in read_sockets:
            # KASUS 1: Ada tamu baru mengetuk pintu Server Utama
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                socket_list.append(sockfd) # Daftarkan tamu baru ke CCTV
                clients[sockfd] = addr
                print(f"[BARU] Client {addr} bergabung")

            # KASUS 2: Ada pesan dari salah satu Client
            else:
                try:
                    data = sock.recv(1024)
                    if data:
                        # Ada pesan, sebarkan (Broadcast)
                        pesan = f"[{clients[sock]}]: {data.decode()}\n"
                        # Kirim ke semua orang kecuali server dan pengirimnya sendiri
                        for client_sock in socket_list:
                            if client_sock != server_socket and client_sock != sock:
                                try:
                                    client_sock.send(pesan.encode())
                                except:
                                    client_sock.close()
                                    if client_sock in socket_list:
                                        socket_list.remove(client_sock)
                    else:
                        # Data kosong artinya koneksi diputus normal (FIN)
                        if sock in socket_list:
                            socket_list.remove(sock)
                        print(f"[KELUAR] Client {clients[sock]} pergi")
                        sock.close()
                        del clients[sock]

                except:
                    # Error koneksi (Force Close)
                    if sock in socket_list:
                        socket_list.remove(sock)
                    sock.close()
                    continue

        # Handle Exception sockets (Error)
        for sock in exception_sockets:
            socket_list.remove(sock)
            sock.close()

if __name__ == "__main__":
    sys.exit(run_chat_server())