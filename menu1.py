from telegram.ext import CommandHandler, Updater, CallbackQueryHandler, CallbackContext
from telegram import ChatAction, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from datetime import datetime
import json
import os
import requests
import logging

# Load bot token
with open('token1.ini', 'r') as file:
    BOT_TOKEN = file.read()
# Create bot
updater = Updater(token=BOT_TOKEN, use_context=True)

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu    

# Add /start handler
def start(update, context):
    print('/start has been called')
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f'Hello! Did you /find or /lose item(s)?'
    )

def find(update, context):
  print('/find has been selected')
  button_list = [
    InlineKeyboardButton("Personal", callback_data = 'find_1'),
    InlineKeyboardButton("Academic", callback_data = 'find_2'),
    InlineKeyboardButton("CCA", callback_data = 'find_3'),
    InlineKeyboardButton("Others", callback_data = 'find_4'),
    InlineKeyboardButton("Main Menu", callback_data= 'find_5')
    ]

  reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
  context.bot.send_message(
      chat_id = update.effective_chat.id, text = main_menu_message(),
      reply_markup=reply_markup
      )

def lose(update, context):
    print('/lose has been selected')
    button_list = [
        InlineKeyboardButton("Personal", callback_data = 'lose_1'),
        InlineKeyboardButton("Academic", callback_data = 'lose_2'),
        InlineKeyboardButton("CCA", callback_data = 'lose_3'),
        InlineKeyboardButton("Others", callback_data = 'lose_4'),
        InlineKeyboardButton("Main Menu", callback_data= 'lose_5')
        ]

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    context.bot.send_message(
        chat_id = update.effective_chat.id, text = main_menu_message(),
        reply_markup=reply_markup
        )

def personal(update, context):
  query = update.callback_query
  context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=sub_menu_message(),
                        reply_markup=personal_keyboard())

def academic(update, context):
  query = update.callback_query
  context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=sub_menu_message(),
                        reply_markup=academic_keyboard())

def cca(update, context):
  query = update.callback_query
  context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=sub_menu_message(),
                        reply_markup=cca_keyboard())

def others(update, context):
  pass         

# and so on for every callback_data option
def first_submenu(update, context):
  pass

def second_submenu(update, context):
  pass

############################ Keyboards #########################################

def personal_keyboard():
  keyboard = [[InlineKeyboardButton('Valuables', callback_data='personal_1')],
              [InlineKeyboardButton('Identification', callback_data='personal_2')],
              [InlineKeyboardButton('Electronic', callback_data='personal_3')],
              [InlineKeyboardButton('Essentials', callback_data='personal_4')],
              [InlineKeyboardButton('Main Menu', callback_data='personal_5')]
              ]
  return InlineKeyboardMarkup(keyboard)



############################# Messages #########################################
def main_menu_message():
  return 'Please choose a category:'

def sub_menu_message():
  return 'Please choose a sub-category:'

def second_menu_message():
  return 'Choose the submenu in second menu:'

############################# Handlers #########################################

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('find', find))
updater.dispatcher.add_handler(CommandHandler('lose', lose))

updater.dispatcher.add_handler(CallbackQueryHandler(personal, pattern='find_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(academic, pattern='find_2'))
updater.dispatcher.add_handler(CallbackQueryHandler(cca, pattern='find_3'))
updater.dispatcher.add_handler(CallbackQueryHandler(others, pattern='find_4'))
updater.dispatcher.add_handler(CallbackQueryHandler(start, pattern='find_5'))

updater.dispatcher.add_handler(CallbackQueryHandler(personal, pattern='lose_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(academic, pattern='lose_2'))
updater.dispatcher.add_handler(CallbackQueryHandler(cca, pattern='lose_3'))
updater.dispatcher.add_handler(CallbackQueryHandler(others, pattern='lose_4'))
updater.dispatcher.add_handler(CallbackQueryHandler(start, pattern='lose_5'))

updater.dispatcher.add_handler(CallbackQueryHandler(others, pattern='personal_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(others, pattern='personal_2'))
updater.dispatcher.add_handler(CallbackQueryHandler(others, pattern='personal_3'))
updater.dispatcher.add_handler(CallbackQueryHandler(others, pattern='personal_4'))
updater.dispatcher.add_handler(CallbackQueryHandler(start, pattern='personal_5'))

updater.start_polling()
print('Bot started!')