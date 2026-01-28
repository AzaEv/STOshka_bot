import telebot
from telebot import types
from huggingface_hub import InferenceClient
import os
import time

# Берем токены из переменных окружения
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
HF_TOKEN = os.environ.get('HF_TOKEN')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = InferenceClient("Qwen/Qwen2.5-7B-Instruct", token=HF_TOKEN)

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Идея"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Стошка на связи. Я Искусственный Интеллект Творческих Коллективов СТО! Напиши "Стошка, " или нажми на кнопку, чтобы я придумал тебе творческий номер', reply_markup=get_main_menu())

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = None
    if message.text == "Идея":
        query = "Придумай яркую идею для студенческого творческого номера."
    elif message.text.lower().startswith("стошка"):
        query = message.text.replace("стошка", "").strip(", ")

    if query:
        bot.send_chat_action(message.chat.id, 'typing')
        try:
            response = client.chat_completion(
                messages=[{"role": "user", "content": query}],
                max_tokens=500
            )
            bot.reply_to(message, response.choices[0].message.content)
        except Exception as e:
            bot.reply_to(message, "Ошибка нейросети. Попробуй позже.")

if __name__ == "__main__":
    print("Бот запускается на Koyeb...")
    bot.infinity_polling()
