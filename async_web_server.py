import asyncio
import os

async def handle_client(reader, writer):
    try:
        # 1. Terima request (non-blocking)
        request = await reader.read(1024)
        if not request:
            writer.close()
            await writer.wait_closed()
            return

        request_text = request.decode('utf-8', errors='ignore')
        headers = request_text.split('\n')
        first_line = headers[0]

        try:
            filename = first_line.split()[1]
        except IndexError:
            writer.close()
            await writer.wait_closed()
            return

        if filename == '/':
            filename = '/index.html'

        filepath = filename.lstrip('/')

        # 2. File handling
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                content = f.read()

            # MIME type
            if filepath.endswith(".html"):
                mime_type = "text/html"
            elif filepath.endswith(".jpg") or filepath.endswith(".png"):
                mime_type = "image/jpeg"
            else:
                mime_type = "text/plain"

            response_header = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {mime_type}\r\n"
                f"Content-Length: {len(content)}\r\n"
                "Connection: close\r\n\r\n"
            )

            writer.write(response_header.encode() + content)
            await writer.drain()
            print(f"[200] {filepath}")

        else:
            error_content = b"<h1>404 Not Found</h1><p>File tidak ditemukan</p>"

            response_header = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(error_content)}\r\n"
                "Connection: close\r\n\r\n"
            )

            writer.write(response_header.encode() + error_content)
            await writer.drain()
            print(f"[404] {filepath}")

    except Exception as e:
        print("[ERROR]", e)
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8080)
    print("=== Async Web Server berjalan di http://localhost:8080 ===")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer dimatikan.")