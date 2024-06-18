from dotenv import load_dotenv
import os
import telebot
import requests
import json

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o token do ambiente
token = os.getenv("token")

# Inicia o bot
bot = telebot.TeleBot(token, parse_mode='HTML')

# Dicionário para armazenar estados dos usuários
user_states = {}

# Estados possíveis
STATE_START = "start"
STATE_CEP = "cep"

# Handler para responder a qualquer mensagem de texto
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id

    if message.text.lower() == '/start' or user_states.get(user_id) != STATE_CEP:
        bot.send_message(
            chat_id=message.chat.id,
            text="<b>Olá {}</b>, eu sou o ChatCEP! Me envie um CEP para que eu possa te informar o endereço correspondente.".format(message.from_user.first_name),
            parse_mode='HTML'
        )
        user_states[user_id] = STATE_CEP
        bot.register_next_step_handler(message, cep)
    else:
        cep(message)

def cep(message):
    try:
        cep_digitado_pelo_usuario = int(message.text)
        response = requests.get('https://viacep.com.br/ws/{}/json/'.format(str(cep_digitado_pelo_usuario)))

        if response.status_code == 200:
            dicionario = json.loads(response.content.decode('utf-8'))

            mensagem = """<b>cep:</b> {0},
<b>logradouro:</b> {1},
<b>complemento:</b> {2},
<b>bairro:</b> {3},
<b>localidade:</b> {4},
<b>uf:</b> {5},
<b>ibge:</b> {6},
<b>gia:</b> {7},
<b>ddd:</b> {8},
<b>siafi:</b> {9},
"""

            bot.send_message(
                chat_id=message.from_user.id,
                text=mensagem.format(
                    dicionario['cep'],
                    dicionario['logradouro'],
                    '🚫' if dicionario['complemento'] == '' else dicionario['complemento'],
                    '🚫' if dicionario['bairro'] == '' else dicionario['bairro'],
                    '🚫' if dicionario['localidade'] == '' else dicionario['localidade'],
                    '🚫' if dicionario['uf'] == '' else dicionario['uf'],
                    '🚫' if dicionario['ibge'] == '' else dicionario['ibge'],
                    '🚫' if dicionario['gia'] == '' else dicionario['gia'],
                    '🚫' if dicionario['ddd'] == '' else dicionario['ddd'],
                    '🚫' if dicionario['siafi'] == '' else dicionario['siafi']
                ),
                parse_mode='HTML'
            )
            show_options(message)  # Exibe os botões após as informações do CEP
        else:
            bot.send_message(chat_id=message.from_user.id, text='🚫 Informações Incorretas. Informe um CEP válido!')
            show_options(message)
    except:
        bot.send_message(chat_id=message.from_user.id, text='🚫 Informações Incorretas. Informe um CEP válido!')
        show_options(message)

def show_options(message):
    bot.send_message(chat_id=message.chat.id, text="Coloque outro CEP:")

def handle_option(message):
    user_id = message.from_user.id
    if message.text == 'Ver outro CEP':
        bot.send_message(chat_id=message.chat.id, text="Por favor, envie um CEP.")
        bot.register_next_step_handler(message, cep)
    else:
        bot.send_message(chat_id=message.chat.id, text="Obrigado por usar o ChatCEP!")
        user_states[user_id] = STATE_START

# Inicia o bot
bot.polling()
