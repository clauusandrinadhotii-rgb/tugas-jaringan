import socket
import json

def cek_mahasiswa(nim):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 6000))

    # 1. Persiapkan Request (Dict)
    request = {
        "command": "GET_MHS",
        "nim": nim
    }

    # 2. Serialisasi & Kirim
    print(f"Mengirim Request untuk NIM: {nim}...")
    client.send(json.dumps(request).encode('utf-8'))

    # 3. Terima & Deserialisasi
    response_bytes = client.recv(4096)
    response = json.loads(response_bytes.decode('utf-8'))

    # 4. Tampilkan Hasil
    print("Respon Server:", json.dumps(response, indent=2))
    client.close()

if __name__ == "__main__":
    # Test cases
    cek_mahasiswa("101") # Ada
    cek_mahasiswa("999") # Tidak ada