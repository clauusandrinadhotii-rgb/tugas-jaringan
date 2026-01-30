import asyncio

async def tcp_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    print("=== Terhubung ke Async Server ===")
    print("Ketik pesan untuk kirim")
    print("Ketik 'bye' untuk keluar\n")

    try:
        while True:
            # Input user (blocking → harus dipisah dengan executor)
            msg = await asyncio.get_event_loop().run_in_executor(
                None, input, "Client > "
            )

            if msg.lower() == 'bye':
                print("[!] Keluar dari koneksi.")
                break

            # Kirim ke server
            writer.write((msg + "\n").encode())
            await writer.drain()

            # Terima balasan server
            data = await reader.read(1024)
            if not data:
                print("[!] Server menutup koneksi.")
                break

            print("Server >", data.decode().strip())

    except Exception as e:
        print("Error:", e)
    finally:
        writer.close()
        await writer.wait_closed()
        print("=== Client ditutup ===")

if __name__ == "__main__":
    try:
        asyncio.run(tcp_client())
    except KeyboardInterrupt:
        print("\nClient dihentikan.")