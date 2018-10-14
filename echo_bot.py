import telebot
import requests
from wit import Wit
import numpy as np
import cloudconvert
from emoji import emojize

#for conversion of ogg to mp3 files
API_KEY ='lilKExBK7e0rTahBoLZRRZZd596ulOaK3l3RCDKJmJ87AA5sp0uMs4eoRQDJgLyi'
api = cloudconvert.Api(API_KEY)

process = api.createProcess({
    "inputformat": "ogg",
    "outputformat": "mp3"
})

#for use of wit.ai
#wit.ai access tokens
server_access_token = '2RKPUURLBLUHTT5TUFQVLAXC5UJU7NH5'
client_access_token = 'A7ECPYJGZT4UIXU5C64CQ46CNAGFNY3E'

#set up wit.ai
server = Wit(server_access_token)

#for setting up of telegram bot
TOKEN = "683169617:AAFwEmNkrQ4HFDWJeqR4uu-yvohc1VIXkmc"
tb = telebot.TeleBot(TOKEN)

updates = tb.get_updates()

@tb.message_handler(commands=['start', 'help'])
def send_welcome(message):
    tb.reply_to(message, "Howdy, how are you doing?")

@tb.message_handler(func=lambda m: True)
def echo_all(message):
    emoji_message = ""
    
    list_message = message.text.split(' ')
    for i in range(len(list_message)):
        process_word = ""
        process_word = ":" + list_message[i] + ":"
        emoji_word = emojize(process_word, use_aliases = True)
        if i == 0:
            emoji_message += emoji_word
        else:
            emoji_message = emoji_message + " " + emoji_word
    new_emoji_message = ""
    for letter in emoji_message:
        if letter != ':':
            new_emoji_message = new_emoji_message + letter
    tb.reply_to(message, new_emoji_message)

    Message_dict = server.message(message.text)
    try:
        emotion = Message_dict ['entities']['sentiment'][0]['value']
        if (emotion == 'positive'):
            tb.reply_to(message, 'I am happy too! :)')
        elif (emotion == 'neutral'):
            tb.reply_to(message, 'What a boring day! :/')
        elif (emotion == 'negative'):
            tb.reply_to(message, 'How can I cheer you up? :(')
    except KeyError:
        tb.reply_to(message, 'Sorry could not detect your happiness level')

@tb.message_handler(content_types=['audio'])
def handle_docs_audio(message):
    fileid = message.audio.file_id

    file_info = tb.get_file(fileid)
    telegram_url = 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path)
    
    file = requests.get(telegram_url)

    with open('movie.mp3', 'wb') as f:
        f.write(file.content)

    Speech_dict_mp3 = server.speech(open('movie.mp3','rb'), None, {'Content-Type':'audio/mpeg3'})

    #tb.reply_to(message, Speech_dict_mp3['_text'])

    emoji_message = ""
    
    list_message = Speech_dict_mp3['_text'].split(' ')
    for i in range(len(list_message)):
        process_word = ""
        process_word = ":" + list_message[i] + ":"
        emoji_word = emojize(process_word, use_aliases = True)
        if i == 0:
            emoji_message += emoji_word
        else:
            emoji_message = emoji_message + " " + emoji_word
    new_emoji_message = ""
    for letter in emoji_message:
        if letter != ':':
            new_emoji_message = new_emoji_message + letter
    tb.reply_to(message, new_emoji_message)

    try:
        emotion = Speech_dict_mp3['entities']['sentiment'][0]['value']
        if (emotion == 'positive'):
            tb.reply_to(message, 'I am happy too! :)')
        elif (emotion == 'neutral'):
            tb.reply_to(message, 'What a boring day! :/')
        elif (emotion == 'negative'):
            tb.reply_to(message, 'How can I cheer you up? :(')
    except KeyError:
        tb.reply_to(message, 'Sorry could not detect your happiness level')

@tb.message_handler(content_types=['voice'])
def handle_docs_voice(message):
    fileidx = message.voice.file_id

    file_infox = tb.get_file(fileidx)
    telegram_urlx = 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_infox.file_path)
    
    filex = requests.get(telegram_urlx)

    with open('movie.ogg', 'wb') as f:
        f.write(filex.content)
    process.start({
        "input": "upload",
        "file": open('movie.ogg', 'rb'),
        "outputformat": "mp3",})
    process.refresh()
    process.wait()
    process.download('movie.mp3')

    Speech_dict_mp3 = server.speech(open('movie.mp3','rb'), None, {'Content-Type':'audio/mpeg3'})

    #tb.reply_to(message, Speech_dict_mp3['_text'])

    emoji_message = ""
    
    list_message = Speech_dict_mp3['_text'].split(' ')
    for i in range(len(list_message)):
        process_word = ""
        process_word = ":" + list_message[i] + ":"
        emoji_word = emojize(process_word, use_aliases = True)
        if i == 0:
            emoji_message += emoji_word
        else:
            emoji_message = emoji_message + " " + emoji_word
    new_emoji_message = ""
    for letter in emoji_message:
        if letter != ':':
            new_emoji_message = new_emoji_message + letter
    tb.reply_to(message, new_emoji_message)

    try:
        emotion = Speech_dict_mp3['entities']['sentiment'][0]['value']
        if (emotion == 'positive'):
            tb.reply_to(message, 'I am happy too! :)')
        elif (emotion == 'neutral'):
            tb.reply_to(message, 'What a boring day! :/')
        elif (emotion == 'negative'):
            tb.reply_to(message, 'How can I cheer you up? :(')
    except KeyError:
        tb.reply_to(message, 'Sorry could not detect your happiness level')
        
tb.polling(none_stop=False, interval=0, timeout=20)

