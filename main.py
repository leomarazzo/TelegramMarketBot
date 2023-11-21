import json
from dotenv import load_dotenv
import os
import telebot

from market_bot import MarketBot


if __name__ == "__main__":
    load_dotenv()
    with open("messages.json", 'r') as f:
        messages = json.load(f)
    bot = telebot.TeleBot(os.getenv("TOKEN"))
    market_bot = MarketBot(bot=bot, lists={}, messages=messages)
    market_bot.register_handlers()
    bot.infinity_polling()