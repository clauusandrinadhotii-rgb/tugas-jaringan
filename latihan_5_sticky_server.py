# latihan_5_sticky_server.py
import socket

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR agar port bisa langsung dipaka ulang setelah server mati
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(('localhost', 5555))
    server.listen(5)
    print("=== Server Framing Siap (Port 5555) ===")

    while True:
        try:
            conn, addr = server.accept()
            print(f"[!] Koneksi dari {addr}")

            # MEMBUAT FILE OBJECT DARI SOCKET
            # Mode 'r' = Read, encoding utf-8
            # Ini memungkinkan kita pakai 'for line in stream'
            with conn:
                stream = conn.makefile('r', encoding='utf-8')

                # Loop ini otomatis membaca per baris (\n)
                # Jika tidak ada \n, dia menunggu (buffer)
                for line in stream:
                    line = line.strip() # Hapus \n di ujung
                    if not line: break

                    print(f"Terima Pesan Utuh: {line}")

                    # Balas juga dengan framing \n
                    conn.send(f"ACK: {line}\n".encode('utf-8'))

            print(f"[!] {addr} terputus.")

        except Exception as e:
            print(f"Error Server: {e}")

if __name__ == "__main__":
    run_server()