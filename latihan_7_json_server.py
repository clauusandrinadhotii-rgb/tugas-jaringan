import socket
import json

# Database dummy dalam memori
DATABASE = {
    "101": {"nama": "klaudia Oktaviani", "prodi": "Teknik Informatika", "ipk": 3.75},
    "102": {"nama": "Siti Aminah", "prodi": "Sistem Informasi", "ipk": 3.90},
    "103": {"nama": "Andi Wijaya", "prodi": "Teknik Komputer", "ipk": 3.50}
}

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 6000))
    server.listen(5)
    print("=== Database Server (JSON) Berjalan di Port 6000 ===")

    while True:
        client, addr = server.accept()
        print(f"[!] Koneksi dari {addr}")

        try:
            # 1. Terima data byte
            request_bytes = client.recv(4096)
            if not request_bytes: break

            # 2. Deserialisasi (Bytes -> String -> Dict)
            request_str = request_bytes.decode('utf-8')
            print(f"DEBUG REQ: {request_str}")

            # Parsing JSON (Bisa error jika format salah)
            request_data = json.loads(request_str)

            # 3. Logika Bisnis (Cek Command)
            command = request_data.get('command')
            nim = request_data.get('nim')

            response = {}

            if command == 'GET_MHS':
                if nim in DATABASE:
                    response = {
                        "status": "SUKSES", 
                        "data": DATABASE[nim]
                    }
                else:
                    response = {"status": "GAGAL", "pesan": "NIM tidak ditemukan"}
            else:
                response = {"status": "ERROR", "pesan": "Perintah tidak dikenali"}

            # 4. Serialisasi (Dict -> String JSON -> Bytes)
            response_bytes = json.dumps(response).encode('utf-8')
            client.send(response_bytes)

        except json.JSONDecodeError:
            error_msg = json.dumps({"status": "ERROR", "pesan": "Format JSON Invalid"}).encode()
            client.send(error_msg)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client.close()

if __name__ == "__main__":
    run_server()