import os
from .config import TOKEN
from .service import SaveDocumentBot
from ..db import User, ScanDocument, Text

bot_instance = SaveDocumentBot(TOKEN)
# bot_instance = SaveDocumentBot(os.environ.get('TOKEN_KEY'))

@bot_instance.message_handler(content_types=['text'], commands=['start'])
def start(message):
    user = User.get_user(chat=message.chat)
    bot_instance.send_message_from_type(user, Text.START_MESSAGE)

@bot_instance.message_handler(content_types=['text'])
def only_message(message):
    user = User.get_user(chat=message.chat)
    bot_instance.send_message_from_type(user, Text.OTHER_MESSAGE)

@bot_instance.message_handler(content_types=['photo'])
def photo_message(message):
    user = User.get_user(chat=message.chat)
    bot_instance.send_message_from_type(user, Text.PHOTO_MESSAGE)


@bot_instance.message_handler(content_types=['document'])
def document_message(message):
    user = User.get_user(chat=message.chat)

    mime_type = message.document.mime_type

    if mime_type.find('image') == -1:
        bot_instance.send_message_from_type(user, Text.DOCUMENT_NOT_TYPE_MESSAGE)
        return
    document = bot_instance.add_document(user, message)

    bot_instance.send_message_from_type(user, Text.DOCUMENT_MESSAGE)