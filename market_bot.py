from dataclasses import dataclass
import os
import tempfile
from typing import Dict
from telebot import TeleBot

from market_list import MarketList


@dataclass
class MarketBot:
    bot: TeleBot
    lists: Dict[str, MarketList]
    messages: dict[str, dict[str, str]]

    def send_welcome(self, message):
        self.bot.reply_to(message, self.messages["welcome"]["en"], parse_mode="MarkdownV2")

    def start_new_list(self, message):
        self.lists[message.chat.id] = MarketList(message.chat.id, [])
        self.bot.send_message(message.chat.id, self.messages["new list"]["en"].format(message.from_user.username))
    
    def add_to_list(self, message):
        if message.chat.id in self.lists:
            self.lists[message.chat.id].add_item(message.text)
            self.bot.reply_to(message, "Added")
            self.bot.send_message(message.chat.id, f"Total: {self.lists[message.chat.id].total()}")
        else:
            self.bot.send_message(message.chat.id, self.messages["no list"]["en"].format(message.from_user.username))

    def print(self, message):
        if message.chat.id in self.lists:
            self.bot.send_message(message.chat.id, self.lists[message.chat.id].serialize(), parse_mode="MarkdownV2")
            self.bot.send_message(message.chat.id, "If you need more details you can use the /print_det command (Probably you will need a wider screen, you can rotate your phone for this).")
        else:
            self.bot.send_message(message.chat.id, self.messages["no list"]["en"].format(message.from_user.username))
    
    def print_det(self, message):
        if message.chat.id in self.lists:
            self.bot.send_message(message.chat.id, self.lists[message.chat.id].serialize_detailed(), parse_mode="MarkdownV2")
        else:
            self.bot.send_message(message.chat.id, self.messages["no list"]["en"].format(message.from_user.username))

    def total(self, message):
        if message.chat.id in self.lists:
            self.bot.send_message(message.chat.id, self.lists[message.chat.id].total())
        else:
            self.bot.send_message(message.chat.id, self.messages["no list"]["en"].format(message.from_user.username))

    def export(self, message):
        if message.chat.id in self.lists:
            with tempfile.TemporaryDirectory() as temp_dir:
                filename = f"{message.from_user.username}.csv"
                path = os.path.join(temp_dir, filename)
                self.lists[message.chat.id].export(path)
                doc = open(path, 'rb')
                self.bot.send_document(message.chat.id, doc)
        else:
            self.bot.send_message(message.chat.id, self.messages["no list"]["en"].format(message.from_user.username))

    def register_handlers(self):
        self.bot.register_message_handler(self.send_welcome, commands=['start', 'help'])
        self.bot.register_message_handler(self.start_new_list, commands=['new'])
        self.bot.register_message_handler(self.add_to_list, regexp="^[\w ]{1,} \d{1,} [\d\.\,]{1,}$")
        self.bot.register_message_handler(self.print, commands=["print"])
        self.bot.register_message_handler(self.print_det, commands=["print_det"])
        self.bot.register_message_handler(self.total, commands=["total"])
        self.bot.register_message_handler(self.export, commands=["export"])