import telebot
from telebot import types
from huggingface_hub import InferenceClient
import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- КОНФИГУРАЦИЯ ---
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
HF_TOKEN = os.environ.get('HF_TOKEN')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = InferenceClient("Qwen/Qwen2.5-7B-Instruct", token=HF_TOKEN)

# --- ЗАГЛУШКА ДЛЯ KOYEB (HEALTH CHECK) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    server = HTTPServer(('0.0.0.0', 8000), HealthCheckHandler)
    print("Health check server started on port 8000", flush=True)
    server.serve_forever()

# --- ЛОГИКА БОТА ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("💡 Идея"))
    bot.send_message(message.chat.id, 'Я Стошка - Искусственный Интеллект студенческий коллективов СТО. Напиши "Стошка, ", чтобы я начал размышлять или нажми кнопку, чтобы я предложил тебе идею творческого номера', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = None
    if message.text == "Идея":
        query = "Придумай яркую идею для студенческого творческого номера."
    elif message.text.lower().startswith("стошка"):
        query = message.text.replace("стошка", "").strip(", ")

    if query:
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            response = client.chat_completion(
                messages=[{"role": "user", "content": query}],
                max_tokens=500
            )
            bot.reply_to(message, response.choices[0].message.content)
        except Exception as e:
            print(f"Error: {e}")

# --- ЗАПУСК ---
if __name__ == "__main__":
    # 1. Запускаем "приманку" для Koyeb в отдельном потоке
    threading.Thread(target=run_health_server, daemon=True).start()
    
    # 2. Запускаем бота
    print("Бот запускается...", flush=True)
    bot.infinity_polling()
