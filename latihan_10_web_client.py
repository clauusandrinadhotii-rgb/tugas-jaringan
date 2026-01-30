import socket

HOST, PORT = '', 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"=== Python Web Server Berjalan di http://localhost:{PORT} ===")

    while True:
        conn, addr = s.accept()
        with conn:
            request = conn.recv(1024).decode()
            path = request.split(' ')[1]

            if path == '/':
                path = '/index.html'
            try:
                with open(path[1:], 'rb') as f:
                    content = f.read()
                response = b'HTTP/1.1 200 OK\n\n' + content
            except FileNotFoundError:
                response = b'HTTP/1.1 404 Not Found\n\nFile Tidak Ditemukan'

            conn.sendall(response)