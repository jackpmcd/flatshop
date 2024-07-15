import os
import telebot
import gkeepapi
from scraper import *
from dotenv import load_dotenv

load_dotenv()

gmail = os.getenv('GMAIL')
master_token = os.getenv('MASTER_TOKEN')
chat_id = os.getenv('CHAT_ID')

keep = gkeepapi.Keep()
keep.authenticate(gmail, master_token)

list_id = os.getenv('LIST_ID')
shopping_list = keep.get(list_id)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

print("Bot is running...")

@bot.message_handler(commands=['add'])
def item_add(message):
    if message.chat.id == int(chat_id): 
        _, *item = message.text.split()

        if item:
            item = ' '.join(item)
            add_to_keep(item)
            bot.set_message_reaction(message.chat.id, message.id, [telebot.types.ReactionTypeEmoji("👍")])
        else:
            bot.reply_to(message, "Please provide a food item to add")
    else:
        bot.reply_to(message, "You're in the wrong place buddy.")

@bot.message_handler(commands=['addlist'])
def list_add(message):
    if message.chat.id == int(chat_id): 
        _, *items = message.text.split()

        if items:
            split_items = ' '.join(items).split(', ')
            for item in split_items:
                add_to_keep(item)
            bot.set_message_reaction(message.chat.id, message.id, [telebot.types.ReactionTypeEmoji("👍")])
        else:
            bot.reply_to(message, "Please provide a list of food items")
    else:
        bot.reply_to(message, "You're in the wrong place buddy.")

@bot.message_handler(commands=['showlist'])
def show_list(message):
    print(message.chat.id, chat_id)
    if message.chat.id == int(chat_id): 
        keep.sync()
        items = [item.text for item in shopping_list.unchecked]
        if len(items) == 0:
            bot.reply_to(message, "Your shopping list is empty")
        else:
            bot.reply_to(message, '\n'.join(items))
    else:
        bot.reply_to(message, "You're in the wrong place buddy.")

@bot.message_handler(commands=['addurl'])
def add_url(message):
    if message.chat.id == int(chat_id): 
        keep.sync()
        _, *url = message.text.split()
        items = [item.text for item in shopping_list.unchecked]
        if url:
            url = ' '.join(url)
            ingredients = extract_nouns(url, items)
            # for ingredient in ingredients:
            #     if ingredient not in items:
            add_to_keep(ingredients)
            bot.set_message_reaction(message.chat.id, message.id, [telebot.types.ReactionTypeEmoji("👍")])
        else:
            bot.reply_to(message, "Please provide a URL")

def add_to_keep(item):
    shopping_list.add(item, False)
    keep.sync()

bot.infinity_polling()
