import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5000))

# ==========================
# AUTHENTIKASI
# ==========================
auth_msg = client.recv(1024).decode('utf-8')   # "kolo: "
print(auth_msg, end="")

password = input()
client.send(password.encode('utf-8'))

auth_result = client.recv(1024).decode('utf-8')
print(auth_result)

if "salah" in auth_result.lower():
    client.close()
    print("Koneksi ditutup oleh server.")
    exit()

# ==========================
# CHAT LOOP
# ==========================
while True:
    try:
        msg = input("Client > ")
        client.send(msg.encode('utf-8'))

        if msg.lower() == 'bye':
            print("[!] Anda keluar dari chat.")
            break

        reply = client.recv(1024).decode('utf-8')
        print(f"Server > {reply}")

        if reply.lower() == 'bye':
            print("[!] Server keluar.")
            break

    except Exception as e:
        print("Error:", e)
        break

client.close()
print("=== Client ditutup ===")