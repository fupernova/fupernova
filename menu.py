from telegram.ext import CommandHandler, Updater, CallbackQueryHandler
from telegram import ChatAction, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import json
import os
import requests
import logging

path = ''
try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)
# Load bot token
with open('token1.ini', 'r') as file:
    BOT_TOKEN = file.read()
# Create bot
updater = Updater(token=BOT_TOKEN, use_context=True)

# Function to build inline menu
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu    

# /start handler
def start(update, context):
    keyboard = [
        InlineKeyboardButton('Option 1', callback_data='m1'),
        InlineKeyboardButton('Option 2', callback_data='m2'),
        InlineKeyboardButton('Option 3', callback_data='m3')
        ]

    reply_markup=InlineKeyboardMarkup(build_menu(keyboard, n_cols=2))
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=main_menu_message(),
        reply_markup=reply_markup
    )


def personal_lost(update, context):
    keyboard = [
        InlineKeyboardButton('Valuables', callback_data=1),
        InlineKeyboardButton('test', callback_data=2)
        ]
  #query = update.callback_query
  context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=main_menu_message(),
                        reply_markup=main_menu_keyboard())

def first_menu(update, context):
  query = update.callback_query
  context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=first_menu_message(),
                        reply_markup=first_menu_keyboard())

def second_menu(update, context):
    keyboard = [
        InlineKeyboardButton('Valuables', callback_data='valuable_lost'),
        InlineKeyboardButton('Idenfication', callback_data='ID_lost'),
        InlineKeyboardButton('Essentials', callback_data='essentials_lost'),
        InlineKeyboardButton('Electronics', callback_data='elec_lost'),
        InlineKeyboardButton('Others', callback_data='personal_others_lost'),
        InlineKeyboardButton('Back to main menu', callback_data='lost_main')
        ]
        reply_markup=build_menu(keyboard, n_col=2)
  query = update.callback_query
  context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text='Choose category'
                        reply_markup=reply_markup)

# and so on for every callback_data option
#def first_submenu(update, context):
  #pass

#def second_submenu(update, context):
  #pass

############################ Keyboards #########################################
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Option 1', callback_data='m1')],
              [InlineKeyboardButton('Option 2', callback_data='m2')],
              [InlineKeyboardButton('Option 3', callback_data='m3')]]
  return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
              [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
              [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################
def main_menu_message():
  return 'Choose the option in main menu:'

def first_menu_message():
  return 'Choose the submenu in first menu:'

def second_menu_message():
  return 'Choose the submenu in second menu:'

############################# Handlers #########################################

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu,
                                                    pattern='m1_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
                                                    pattern='m2_1'))

updater.start_polling()