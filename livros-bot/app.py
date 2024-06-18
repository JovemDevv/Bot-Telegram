from dotenv import load_dotenv
import os
import telebot
from telebot import types

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o token do ambiente
token = os.getenv("token")

# Inicia o bot
bot = telebot.TeleBot(token, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def handler_start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('📚 Livros', callback_data='/chatbot_livros'),
        types.InlineKeyboardButton('Acesse para ver mais', url='https://www.amazon.com.br/')
    )

    bot.send_message(chat_id=message.from_user.id, text=f'<b>Sr(a) {message.from_user.first_name}</b> bem-vindo! Escolha uma das opções abaixo:',reply_to_message_id=message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == '/chatbot_livros':
        # Action typing(digitando...)
        bot.send_chat_action(chat_id=call.from_user.id, action='typing')
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton('📚 1. Aventuras na Terra do Codigo', callback_data='/chatbot_aventuras'),
            types.InlineKeyboardButton('📚 2. Fundamentos da programacao pascal C C java 1', callback_data='/chatbot_fundamentos')
        )

        bot.send_message(chat_id=call.from_user.id, text=f'<b>Sr(a) {call.from_user.first_name}</b> Escolha um dos livros abaixo:', reply_markup=markup)
    
    elif call.data == '/chatbot_aventuras':
        bot.send_chat_action(chat_id=call.from_user.id, action='typing')
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('⬅ Voltar', callback_data='/chatbot_voltar')
        )

        bot.send_document(chat_id=call.from_user.id, document=open('livros/Aventuras_na_Terra_do_Codigo.pdf', 'rb'), caption='📚 <b>Livro escolhido:</b> <i>Aventuras na Terra do Codigo.pdf</i>', reply_markup=markup)

    elif call.data == '/chatbot_fundamentos':
        bot.send_chat_action(chat_id=call.from_user.id, action='typing')
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('⬅ Voltar', callback_data='/chatbot_voltar')
        )

        bot.send_document(chat_id=call.from_user.id, document=open('livros/Fundamentos_da_programacao_pascal_C_C_java_1.pdf', 'rb'), caption='📚 <b>Livro escolhido:</b> <i>Fundamentos da programacao pascal C C java 1.pdf</i>', reply_markup=markup)

    elif call.data == '/chatbot_voltar':
        bot.send_chat_action(chat_id=call.from_user.id, action='typing')
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton('📚 Livros', callback_data='/chatbot_livros'),
            types.InlineKeyboardButton('Acesse para ver mais', url='https://www.amazon.com.br/')
        )

        bot.send_message(chat_id=call.from_user.id, text=f'<b>Sr(a) {call.from_user.first_name}</b> bem-vindo! Escolha uma das opções abaixo:', reply_markup=markup)


bot.polling()
