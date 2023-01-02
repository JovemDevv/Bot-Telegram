# Bot
Automatizador de envio de mensagem no Telegram. 

Inicialmente precisamos gerar um token para nosso bot. O token é necessário para acessar a API do Telegram e instalar as dependências necessárias.
Vá ao BotFather (se você abri-lo na área de trabalho, certifique-se de ter o aplicativo Telegram) e, em seguida, crie um novo bot enviando o '/newbot' comando. Siga as etapas até obter o nome de usuário e o token para o seu bot.

## Explicação simples de como funciona:

Quando o usuário inicia o bot, ele pode enviar mensagens e o bot responderá com o horário de estudo para o dia da semana correspondente.

A classe TelegramBot possui três métodos:

* iniciar(): Esse método é responsável por fazer o bot ficar "online" e pronto para receber mensagens. Ele faz isso em um loop infinito, verificando se há atualizações de mensagens (com o método obter_mensagens()). Se houver, o bot irá processar as mensagens e enviar respostas (com o método responder()).
obter_mensagens(update_id): Esse método faz uma requisição à API do telegram para obter novas mensagens. A variável update_id é usada para garantir que o bot não processe mensagens já lidas.
* criar_resposta(texto): Esse método recebe uma mensagem do usuário e retorna a resposta do bot de acordo com o conteúdo da mensagem. Se a mensagem for "voltar", o bot enviará uma mensagem de boas vindas e as opções de dias da semana. Se a mensagem for um número de 1 a 5, o bot enviará o horário de estudo para o dia da semana correspondente. Se a mensagem for qualquer outra coisa, o bot enviará uma mensagem de erro dizendo que não entendeu o que o usuário quer dizer.
* responder(resposta, chat_id): Esse método envia a resposta do bot para o usuário que enviou a mensagem. O parâmetro chat_id é o ID da conversa entre o usuário e o bot, e é usado para garantir que a resposta seja enviada para a conversa correta.
