from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

class TelegramBot:
    def __init__(self):
        token = os.getenv('Api_chave')
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_mensagens(update_id)
            if atualizacao:  # verifica se atualizacao é diferente de None
                mensagens = atualizacao['resultado']
                if mensagens:
                    for mensagem in mensagens:
                        update_id = mensagem['update_id']
                        chat_id = mensagem['mensagem']['from']['id']
                        texto = mensagem['mensagem']['text']
                        resposta = self.criar_resposta(texto)
                        self.responder(resposta,chat_id)

    def obter_mensagens(self, update_id):
        link_request = f'{self.url_base}getUpdates?timeout=1000&offset='
        resultado = requests.get(link_request)
        return json.loads(resultado.content)


    def criar_resposta(self, texto):
        if texto.lower() == 'voltar':
            return f'''Olá bem vindo ao Hora de Estudar. Digite o dia
            da semana{os.linesep} 1 - Segunda{os.linesep}
            2 - Terça{os.linesep} 3 - Quarta{os.linesep} 4 - Quinta{os.linesep}
            5 - Sexta{os.linesep}'''
        elif texto.lower() == '1':
            return 'Segunda: Python'
        elif texto.lower() == '2':
            return 'Terça: HTML e CSS'
        elif texto.lower() == '3':
            return 'Quarta: JavaScript'
        elif texto.lower() == '4':
            return 'Quinta: Inglês'
        elif texto.lower() == '5':
            return 'Sexta: Algoritmos'
        else:
            return 'Desculpe, eu não entendi o que você quer dizer. Por favor, digite novamente.'

        
    def responder(self, resposta,chat_id):
        link_de_envio = f"{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}"
        requests.get(link_de_envio)
    
bot = TelegramBot()
bot.iniciar()
