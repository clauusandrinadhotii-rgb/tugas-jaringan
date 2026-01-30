import asyncio

async def handle_client(reader, writer):
    """
    Coroutine ini akan dijalankan untuk SETIAP client yang connect.
    Bayangkan ini sebagai 'Langkah Catur' untuk satu meja.
    """
    addr = writer.get_extra_info('peername')
    print(f"[BARU] Koneksi dari {addr}")

    try:
        while True:
            # 1. Baca Data (Non-Blocking)
            # keyword 'await' artinya: "Tunggu data masuk, tapi JANGAN BLOKIR server."
            # "Silakan server urus client lain dulu. Kalau data sudah ada, bangunkan saya."
            data = await reader.read(100) # Baca maksimal 100 byte

            if not data:
                print(f"[PUTUS] {addr} menutup koneksi.")
                break

            message = data.decode().strip()
            print(f"[{addr}] Mengirim: {message}")

            # 2. Proses & Balas
            response = f"Echo: {message}\n"
            writer.write(response.encode())

            # 3. Pastikan data terkirim (Drain buffer)
            await writer.drain()

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        writer.close()
        await writer.wait_closed() # Pastikan socket benar-benar tutup

async def main():
    # Membuat Server Async
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'=== Async Server Berjalan di {addrs} ===')

    # Biarkan server berjalan selamanya
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    # Memulai Event Loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer Dimatikan.")