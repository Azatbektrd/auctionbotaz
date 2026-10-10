import threading
import asyncio
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

# Простой веб-сервер для порта 7860, чтобы Hugging Face считал проект активным
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_web():
    server = HTTPServer(("0.0.0.0", 7860), SimpleHandler)
    server.serve_forever()

# Запускаем веб-сервер в фоновом потоке
threading.Thread(target=run_web, daemon=True).start()

# Импортируем и запускаем вашего основного бота из bot.py
import bot

if __name__ == "__main__":
    asyncio.run(bot.main())
  
