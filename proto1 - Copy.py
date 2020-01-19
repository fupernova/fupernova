from telegram.ext import CommandHandler, Updater, CallbackQueryHandler, MessageHandler, ConversationHandler, Filters
from telegram import ChatAction, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Message
from datetime import datetime
import json
import os
import requests
import logging

trigger_find=False
trigger_lose=False

# Load bot token
with open('token1.ini', 'r') as file:
    BOT_TOKEN = file.read()
# Create bot
updater = Updater(token=BOT_TOKEN, use_context=True)

RESPONSE, NO_PIC = range(2)

############################## Conversation handlers ###########################################
def report(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please upload a photo and a brief description of the item you found. (Note: It will not work if no picture is sent.)'
    )
    return RESPONSE

def response(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    update.message.reply_text('Thank you for your report. It will now be filed in our records.')
    return ConversationHandler.END


def no_pic(update, context):
    user = update.message.from_user
    update.message.reply_text('Please submit a picture of the item')
    return RESPONSE

def cancel(update, context):
    user = update.message.from_user
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END

# Function to construct inline keyboard
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
  global trigger_find
  trigger_find=True
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
    global trigger_lose
    trigger_lose=True
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
    print('personal has been selected')
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=sub_menu_message(),
                        reply_markup=personal_keyboard())

def academic(update, context):
    print('academic has been selected')
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=sub_menu_message(),
                        reply_markup=academic_keyboard())

def cca(update, context):
    print('cca has been selected')
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=sub_menu_message(),
                        reply_markup=cca_keyboard())

def others(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Others has been selected'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.'
    )
    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost.'
    )
def valuables(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Valuables has been selected.'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.'
    )
    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost.'
    )

def identification(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Identification has been selected.'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.'
    )
    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost.'
    )

def electronic(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Electronics has been selected.'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.',
    )

    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost.'
    )
        img_url='https://imgur.com/rIglB1C'

        context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=img_url,
        caption='Apple laptop with black sleeve found at Cinnamon College dining hall at 4.30pm',
        parse_mode=ParseMode.MARKDOWN
    )

def essentials(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Essentials has been selected.'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.'
    )
    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost.'
    )

def notes(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Notes has been selected.'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.'
    )
    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost.'
    )

def textbooks(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Textbooks has been selected.'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.'
    )
    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost.'
    )

def library_books(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Library books has been selected.'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.'
    )
    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost.'
    )

def physical_assignments(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Assignments has been selected.'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.'
    )
    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost.'
    )

def sports_equipment(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Sports equipment has been selected.'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.'
    )
    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost.'
    )

def costumes_attires(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Costumes has been selected.'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.'
    )
    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost'
    )

def instruments(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Instruments has been selected.'
    )
    global trigger_lose
    global trigger_find
    if trigger_find:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Type /report to submit a report for an item you found.'
    )
    else:
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Please check if the following entries matches the item you lost.'
    )

############################ Keyboards #########################################

def personal_keyboard():
  keyboard = [[InlineKeyboardButton('Valuables', callback_data='personal_1')],
              [InlineKeyboardButton('Identification', callback_data='personal_2')],
              [InlineKeyboardButton('Electronic', callback_data='personal_3')],
              [InlineKeyboardButton('Essentials', callback_data='personal_4')],
              [InlineKeyboardButton('Main Menu', callback_data='personal_5')]
              ]
  return InlineKeyboardMarkup(keyboard)

def academic_keyboard():
  keyboard = [[InlineKeyboardButton('Notes', callback_data='academic_1')],
              [InlineKeyboardButton('Textbooks', callback_data='academic_2')],
              [InlineKeyboardButton('Library Books', callback_data='academic_3')],
              [InlineKeyboardButton('Physical Assignments', callback_data='academic_4')],
              [InlineKeyboardButton('Main Menu', callback_data='academic_5')]
              ]
  return InlineKeyboardMarkup(keyboard)

def cca_keyboard():
  keyboard = [[InlineKeyboardButton('Sports Equipment', callback_data='cca_1')],
              [InlineKeyboardButton('Costumes/Attires', callback_data='cca_2')],
              [InlineKeyboardButton('Instruments', callback_data='cca_3')],
              [InlineKeyboardButton('Main Menu', callback_data='cca_4')] 
              ]
  return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################
def main_menu_message():
  return 'Please choose a category:'

def sub_menu_message():
  return 'Please choose a sub-category:'

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

updater.dispatcher.add_handler(CallbackQueryHandler(valuables, pattern='personal_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(identification, pattern='personal_2'))
updater.dispatcher.add_handler(CallbackQueryHandler(electronic, pattern='personal_3'))
updater.dispatcher.add_handler(CallbackQueryHandler(essentials, pattern='personal_4'))
updater.dispatcher.add_handler(CallbackQueryHandler(start, pattern='personal_5'))

updater.dispatcher.add_handler(CallbackQueryHandler(notes, pattern='academic_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(textbooks, pattern='academic_2'))
updater.dispatcher.add_handler(CallbackQueryHandler(library_books, pattern='academic_3'))
updater.dispatcher.add_handler(CallbackQueryHandler(physical_assignments, pattern='academic_4'))
updater.dispatcher.add_handler(CallbackQueryHandler(start, pattern='academic_5'))

updater.dispatcher.add_handler(CallbackQueryHandler(sports_equipment, pattern='cca_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(costumes_attires, pattern='cca_2'))
updater.dispatcher.add_handler(CallbackQueryHandler(instruments, pattern='cca_3'))
updater.dispatcher.add_handler(CallbackQueryHandler(start, pattern='cca_4'))

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('report', report)],

    states={
        RESPONSE: [MessageHandler(Filters.photo, response)],
        NO_PIC: [MessageHandler(Filters.text, no_pic)]
    },
     fallbacks=[CommandHandler('cancel', cancel)]
)

dp = updater.dispatcher
dp.add_handler(conv_handler)

updater.start_polling()
print('Bot started!')