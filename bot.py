import os
import telebot
import gkeepapi
from dotenv import load_dotenv

load_dotenv()

gmail = os.getenv('GMAIL')
master_token = os.getenv('MASTER_TOKEN')

keep = gkeepapi.Keep()
keep.authenticate(gmail, master_token)

list_id = os.getenv('LIST_ID')
shopping_list = keep.get(list_id)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

print("Bot is running...")

@bot.message_handler(commands=['addfood'])
def food_add(message):
    _, *item = message.text.split()

    if item:
        item = ' '.join(item)
        add_to_keep(item)
        bot.set_message_reaction(message.chat.id, message.id, [telebot.types.ReactionTypeEmoji("👍")])
    else:
        bot.reply_to(message, "Please provide a food item to add")

@bot.message_handler(commands=['addlist'])
def list_add(message):
    _, *items = message.text.split()

    if items:
        split_items = ' '.join(items).split(', ')
        for item in split_items:
            add_to_keep(item)
        bot.set_message_reaction(message.chat.id, message.id, [telebot.types.ReactionTypeEmoji("👍")])
    else:
        bot.reply_to(message, "Please provide a list of food items")

@bot.message_handler(commands=['showlist'])
def show_list(message):
    print("Here is what is in your shopping list: ")
    items = [item.text for item in shopping_list.unchecked]
    if len(items) == 0:
        bot.reply_to(message, "Your shopping list is empty")
    bot.reply_to(message, '\n'.join(items))

def add_to_keep(item):
    shopping_list.add(item, False)
    print("added to keep: ", item)
    keep.sync()

bot.infinity_polling()
