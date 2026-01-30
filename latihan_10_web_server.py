import socket

def handle_client(client_socket):
    # 1. Terima Request Browser
    request = client_socket.recv(1024).decode('utf-8')

    # Validasi: Kadang browser kirim koneksi kosong
    if not request:
        client_socket.close()
        return

    # 2. Parsing Request Line untuk cari nama file
    # Request: "GET /index.html HTTP/1.1 ..."
    headers = request.split('\n')
    first_line = headers[0]

    try:
        # Ambil bagian path: "/index.html"
        filename = first_line.split()[1]
    except IndexError:
        client_socket.close()
        return

    # Ubah "/" jadi "/index.html" (Default Page)
    if filename == '/':
        filename = '/index.html'

    # Hapus slash depan agar bisa dibaca os.path. " /index.html" -> "index.html"
    filepath = filename.lstrip('/')

    try:
        # 3. Coba Buka File
        # Mode 'rb' (Read Binary) penting agar bisa baca Gambar juga
        with open(filepath, 'rb') as f:
            content = f.read()

        # 4. Susun Response SUKSES (200 OK)
        response_header = "HTTP/1.1 200 OK\r\n"

        # Deteksi Content-Type sederhana
        if filepath.endswith(".html"):
            mime_type = "text/html"
        elif filepath.endswith(".jpg") or filepath.endswith(".png"):
            mime_type = "image/jpeg"
        else:
            mime_type = "text/plain"

        response_header += f"Content-Type: {mime_type}\r\n"
        response_header += f"Content-Length: {len(content)}\r\n"
        response_header += "Connection: close\r\n\r\n" # Header ditutup dengan dua enter (\r\n\r\n)

        # Kirim Header + Body
        client_socket.send(response_header.encode('utf-8') + content)
        print(f"[200] Mengirim {filepath}")

    except FileNotFoundError:
        # 5. Handle Error 404
        error_content = "<h1>404 Not Found</h1><p>File tidak ditemukan di Server.</p>"

        response_header = "HTTP/1.1 404 Not Found\r\n"
        response_header += "Content-Type: text/html\r\n"
        response_header += f"Content-Length: {len(error_content)}\r\n"
        response_header += "Connection: close\r\n\r\n"

        client_socket.send(response_header.encode('utf-8') + error_content.encode('utf-8'))
        print(f"[404] File {filepath} tidak ada")

    client_socket.close()

def run_web_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    print("=== Python Web Server Berjalan di http://localhost:8080 ===")

    while True:
        client, addr = server.accept()
        handle_client(client)

if __name__ == "__main__":
    run_web_server()