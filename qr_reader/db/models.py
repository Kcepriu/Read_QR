import mongoengine as me
import json
from datetime import datetime


from ..image import IMAGE_PR

me.connect('scan_documents')

class User(me.Document):
    user_id = me.IntField(unique=True, required=True)
    name = me.StringField(max_length=255)
    telephone = me.StringField(min_length=10, max_length=12, regex='^[0-9]*$')

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_user(cls, chat):
        user = cls.objects(user_id=chat.id)
        if not user:
            try:
                name = chat.last_name + ' ' + chat.first_name
            except:
                pass
            user = cls.objects.create(user_id=chat.id, name=name)
        else:
            user = user[0]
        return user

class InfoQR_Code(me.EmbeddedDocument):
    qr_nom = me.StringField(max_length=11)
    qr_date = me.DateField()
    qr_sum = me.DecimalField()
    qr_uid = me.StringField(max_length=36)
    qr_uid_client = me.StringField(max_length=36)

class ScanDocument(me.Document):
    user = me.ReferenceField(User, reverse_delete_rule=me.DENY)
    date = me.DateTimeField(default=datetime.now())

    file_id = me.StringField(max_length=100)
    file_name = me.StringField(max_length=255)
    file_size = me.IntField()

    file_path = me.StringField(max_length=255)
    data_file = me.FileField()
    mime_type = me.StringField(max_length=255)

    auto_determination = me.BooleanField(default=False)
    info_qr_code = me.EmbeddedDocumentField(InfoQR_Code)


    @classmethod
    def add_document(cls, user, document_message):
        document = cls.objects.create(user=user,
                                     file_id = document_message.file_id,
                                     file_name = document_message.file_name,
                                     file_size = document_message.file_size,
                                     mime_type = document_message.mime_type)
        return document

    def get_qr_cod(self):
        _data_file = self.data_file.read()

        if not _data_file:
            return

        qr_image = IMAGE_PR(byte_string=_data_file)

        qr_code = qr_image.auto_find_qr_code()

        if qr_code:
            qr_code_json = json.loads(qr_code)
            qr_date = qr_code_json.get('Дата', '01.01.1970')

            self.info_qr_code = InfoQR_Code(
                qr_nom = qr_code_json.get('Номер', ''),
                qr_date = datetime.strptime(qr_date, '%d.%m.%Y'),
                qr_sum = qr_code_json.get('Сумма', ''),
                qr_uid = qr_code_json.get('UID', ''),
                qr_uid_client = qr_code_json.get('UIDКонтрагент', ''))



        qr_image.resize_image()

        self.data_file.replace(qr_image.image_to_byte, content_type='image/jpeg')
        self.mime_type = self.data_file.content_type
        self.file_size = self.data_file.length
        self.auto_determination = True
        self.save()
        return True

class Text(me.Document):
    START_MESSAGE = 'start_message'
    OTHER_MESSAGE = 'others_message'
    PHOTO_MESSAGE = 'photo_message'
    DOCUMENT_MESSAGE = 'document_message'
    DOCUMENT_NOT_TYPE_MESSAGE = 'document_message_not_type_message'

    TITLES_CONSTANT = (
        (START_MESSAGE, 'start message'),
        (OTHER_MESSAGE, 'others message'),
        (PHOTO_MESSAGE, 'photo message'),
        (DOCUMENT_MESSAGE, 'document message'),
        (DOCUMENT_NOT_TYPE_MESSAGE, 'document message not type message')
    )

    title = me.StringField(required=True, choices=TITLES_CONSTANT, unique=True)
    body = me.StringField(min_length=2, max_length=4096)

    @classmethod
    def get_body(cls, title_):
        try:
            _text = cls.objects.get(title=title_)
        except me.DoesNotExist:
            return 'Not text from  - ' + str(title_)

        return _text.body
