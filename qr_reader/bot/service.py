from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from ..db import User, ScanDocument, Text
from ..image import PDF_TO_JPEG

class SaveDocumentBot(TeleBot):
    # Відправляє повідомлення
    def send_message_from_type(self, user: User, type_message: Text.TITLES_CONSTANT):
        text = Text.get_body(type_message)
        result = self.send_message(user.user_id, text)
        return result

    # Створює документ в базі, на основі отрманого повідомлення
    def add_document(self, user: User, message):
        document = ScanDocument.add_document(user, message.document)
        self.get_url_file(document)
        return document

    # отримуємо урл файла і зберігаємо його в базі
    def get_url_file(self, document: ScanDocument):
        try:
            message = self.get_file(document.file_id)
        except ApiTelegramException:
            return

        document.file_path = message.file_path
        self.get_data_file(document, False)
        document.save()
        document.get_qr_cod()

        return True

    # Отримуємо дані файлу із нету і зберігаємо в базі
    def get_data_file(self, document, save=True):
        if not document.file_path:
            return
        mime_type = document.mime_type
        file = self.download_file(document.file_path)

        if mime_type.find('pdf') != -1:
            pdf_to_jpeg = PDF_TO_JPEG(file)

            print(222222222222222222222222222)
            print(type(file))

            file = pdf_to_jpeg.convert_pdf_to_jpeg()

            print(1111111111111111111111111)
            print(type(file))
            mime_type = 'image/jpeg'

        if not file:
            return

        document.data_file.put(file, content_type=mime_type)
        if save:
            document.save()

#------------------------------------------
    def test_add(self):
        doc = ScanDocument.objects(id='5fa9508d3a2f548d40bc754b').get()
        if doc:
            doc.get_qr_cod()

            print('OK')


if __name__ == '__main__':
   pass




