from telegram.ext import CommandHandler, Updater, CallbackQueryHandler, CallbackContext
from telegram import ChatAction, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from datetime import datetime
import json
import os
import requests
import logging

# Load bot token
with open('token.ini', 'r') as file:
    BOT_TOKEN = file.read()

# Create the bot
updater = Updater(token=BOT_TOKEN, use_context=True)

# Add /start handler
def start(update, context):
    print('/start has been called')
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f'Bot started! Did you /find or /lost item(s)?'
    )

# Add menu for categories
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu    

# Add lost handler
def lost (update, context):
    button_list = [
        InlineKeyboardButton("Personal", callback_data = 'personal_lost'),
        InlineKeyboardButton("Academic", callback_data = 'acad_lost'),
        InlineKeyboardButton("CCA", callback_data = 'cca_lost'),
        InlineKeyboardButton("Others", callback_data = 'others_lost')
        ]

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    context.bot.send_message(
        chat_id = update.effective_chat.id, text = "Please choose the category of item you found.",
        reply_markup=reply_markup
        )

# Add find handler
def find (update, context):
    button_list = [
        InlineKeyboardButton("Personal", callback_data = 'personal_find'),
        InlineKeyboardButton("Academic", callback_data = 'acad_find'),
        InlineKeyboardButton("CCA", callback_data = 'cca_find'),
        InlineKeyboardButton("Others", callback_data = 'others_find')
        ]

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    context.bot.send_message(
        chat_id = update.effective_chat.id, text = "Please choose from these categories",
        reply_markup=reply_markup
        )

# Option for reporting lost personal items
def personal_lost(update, context):
    keyboard = [
        InlineKeyboardButton('Valuables', callback_data='valuable_lost'),
        InlineKeyboardButton('Idenfication', callback_data='ID_lost'),
        InlineKeyboardButton('Essentials', callback_data='essentials_lost'),
        InlineKeyboardButton('Electronics', callback_data='elec_lost'),
        InlineKeyboardButton('Others', callback_data='personal_others_lost'),
        InlineKeyboardButton('Back to main menu', callback_data='lost_main')
        ]

    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=3))
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Please further specify category of personal item found.',
       reply_markup=reply_markup
        )

def valuable_lost(update, context):
    keyboard = [
        InlineKeyboardButton('Back to main menu', callback_data='lost_main')
    ]

    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text='Please further specify category of personal item found'
                        #reply_markup=reply_markup
                        )

def ID_lost(update, context):
    keyboard = [
        InlineKeyboardButton('Back to main menu', callback_data='lost_main')
    ]

    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text='Please further specify category of personal item found'
                        #reply_markup=reply_markup
                        )

def essentials_lost(update, context):
    keyboard = [
        InlineKeyboardButton('Back to main menu', callback_data='lost_main')
    ]

    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=3))
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text='Please further specify category of personal item found'
                        #reply_markup=reply_markup
                        )

def elec_lost(update, context):
    keyboard = [
        InlineKeyboardButton('Back to main menu', callback_data='lost_main')
    ]

    query = update.callback_query
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=3))
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text='Please further specify category of personal item found'
                        #reply_markup=reply_markup
                        )

def personal_others_lost(update, context):
    keyboard = [
        InlineKeyboardButton('Back to main menu', callback_data='lost_main')
    ]

    query = update.callback_query
    #reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=3))
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text='Please further specify category of personal item found'
                        reply_markup=InlineKeyboardMarkup(build_menu(keyboard, n_cols=3)
                        )



############################# HANDLERS ########################################
updater.dispatcher.add_handler(
    CommandHandler('start', start)
)

updater.dispatcher.add_handler(
    CommandHandler('lost', lost)
)

updater.dispatcher.add_handler(
    CommandHandler('find', find)
)

updater.dispatcher.add_handler(
    CallbackQueryHandler(lost, pattern='lost_main')
)

updater.dispatcher.add_handler(
    CallbackQueryHandler(personal_lost, pattern='personal_lost')
)

updater.dispatcher.add_handler(
    CallbackQueryHandler(valuable_lost, pattern='valuable_lost')
)
updater.dispatcher.add_handler(
    CallbackQueryHandler(essentials_lost, pattern='essentials_lost')
)
updater.dispatcher.add_handler(
    CallbackQueryHandler(elec_lost, pattern='elec_lost')
)

updater.dispatcher.add_handler(
    CallbackQueryHandler(personal_others_lost, pattern='personal_others_lost')
)









































# Start the bot
updater.start_polling()
print('Bot started!')

# Wait for the bot to stop
updater.idle()
