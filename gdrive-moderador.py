from telebot.async_telebot import AsyncTeleBot
import asyncio
import aiofiles


token = '6911261815:AAEk1_jZTeCZR_EiYXNP0d2FBKK_qwQ900A'
bot = AsyncTeleBot(token)
adm = '673195223'

mensagens_blacklist_venda =  ['pv', 'chama','vendo', 'preço', 'dinheiro', 'compra', 'comprar', 'Vip']


@bot.message_handler(func=lambda message: message.new_chat_members is not None)
async def welcome_new_members(message):
    # Envie uma mensagem de boas-vindas para o usuário que acabou de entrar no grupo
    for new_member in message.new_chat_members:
        await bot.send_message(message.chat.id, f"Bem-vindo, {new_member.first_name}!, 😊Este é um grupo gratuito, você pode contribuir com este projeto com o comando /doacao. Você também pode pedir um curso ao administrador com o comando /pedido nome_do_curso")
       
@bot.message_handler(commands=['pedido'])
async def pedidos(message):
    async with aiofiles.open('usuarios.txt', 'a') as f:
        await f.write(f"{message.from_user.id}\n")
    async with aiofiles.open('logs.txt', 'a') as log:
        await log.write(f"{message.from_user.username}@{message.from_user.id} usou o comando /pedidos  \n")
        
    curso = ' '.join(message.text.split()[1:])
    if curso == '':
        await bot.send_message(message.chat.id, "Por favor, digite o nome do curso que você deseja pedir.")
    else:    
        await bot.reply_to(message, f"Você enviou o seu pedido do curso: *{curso}* Um administrador foi notificado. Você será marcado assim que o curso estiver disponivel  ✅")
        await bot.send_message(adm, f"Um novo pedido foi enviado pelo usuário {message.from_user.username} com o curso *{curso}*")


@bot.message_handler(commands=['doacao'])
async def doacao(message):
    async with aiofiles.open('usuarios.txt', 'a') as f:
        await f.write(f"{message.from_user.id}\n")
    async with aiofiles.open('logs.txt', 'a') as log:
        await log.write(f"{message.from_user.username}@{message.from_user.id} usou o comando /doacao  \n")
    
    await bot.reply_to(message, "Você pode fazer uma doação de qualquer valor para ajudar esse projeto😊\n\nQRCode:\n\n 00020126580014BR.GOV.BCB.PIX01360578e8ae-f5b3-48c1-a7ac-94318f78ca6d5204000053039865802BR5917Rafael Souza Lima6009SAO PAULO621405104BxhovghWG6304B6D6\n\nOu link de pagamento:\n https://nubank.com.br/cobrar/496rb/6591cc12-eead-453e-a538-b8ac05e68151")
    

@bot.message_handler(commands=['verificados'])
async def verificados(message):
    async with aiofiles.open('usuarios.txt', 'a') as f:
        await f.write(f"{message.from_user.id}\n")
    async with aiofiles.open('logs.txt', 'a') as log:
        await log.write(f"{message.from_user.username}@{message.from_user.id} usou o comando /verificados  \n")
    verificados = []
    async with aiofiles.open('verificados.txt', 'r') as f:
        usuarios = await f.readlines()
        for usuario in usuarios:
            verificados.append(f'@{str(usuario.strip())}')
        if verificados:
            await bot.reply_to(message, f"Os usuários verificados são:\n\n{'  -  '.join([str(usuario) for usuario in verificados])}")
        else:
            await bot.reply_to(message, "Nenhum vendedr foi verificado ainda, não recomendamos fazer nenhum pagamento para.")

@bot.message_handler(commands=['regras'])
async def regras(message):
    await bot.reply_to(message, '''Regras do grupo:\n\n1. Não fale nada ofensivo, não seja abusivo e não faça spam.\n2. Não divulgue nada que não seja de interesse ao grupo
3. Não divulgue links sem autorizaçao de um administrador \n4. Não Venda nada sem permissão de um administrador 
                       ''')

@bot.message_handler(commands=['addverificado'])
async def addverificado(message):
    if message.from_user.id == int(adm):
        async with aiofiles.open('verificados.txt', 'a') as f:
            await f.write(f"{message.text.split()[1]}\n")
        await bot.reply_to(message, f"O vendedor {message.text.split()[1]} foi adicionado como verificado.")
    else:
        await bot.reply_to(message, "Você não tem permissão para isso.")
        
# remover verificado do txt
@bot.message_handler(commands=['remoververificado'])
async def remoververificado(message):
    if message.from_user.id == int(adm):
        async with aiofiles.open('verificados.txt', 'r') as f:
            usuarios = await f.readlines()
        async with aiofiles.open('verificados.txt', 'w') as f:
            for usuario in usuarios:
                if usuario.strip() != message.text.split()[1]:
                    await f.write(usuario)
        await bot.reply_to(message, f"O vendedor {message.text.split()[1]} foi removido como verificado.")
    else:
        await bot.reply_to(message, "Você não tem permissão para isso.")

@bot.message_handler(commands=['logs'])
async def logs(message):
    if message.from_user.id == int(adm):
        async with aiofiles.open('logs.txt', 'r') as f:
            logs = await f.read()
        await bot.send_message(message.from_user.id, logs)
    

@bot.message_handler(commands=['addblacklist'])
async def addblacklist(message):
    if message.from_user.id == int(adm):
        palavra = ''.join(message.text.split()[1])
        mensagens_blacklist_venda.append(palavra)
        await bot.reply_to(message, f"blacklist atualizada")
        
    else:
        await bot.reply_to(message, "Você não tem permissão para isso.")


@bot.message_handler(func=lambda message: True)
async def start(message):
    mensagem = message.text.lower()
    for palavra in mensagens_blacklist_venda:
        if palavra in mensagem:
            await bot.send_message(message.chat.id, '❌❌❌❌Tome Cuidado ao comprar conteudos de usuarios não autorizados por um administrador, não chame ninguem no privado, e não faça nenhum pagamento. digite o comando /verificados, e saiba quais são os vendedores verificados pela administração')
            print(message.from_user.id)
            break
async def  main():
    try:
        await bot.polling(none_stop=True)
    except Exception as e:
        print(e)
asyncio.run(main())