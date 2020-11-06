import mongoengine as me
from datetime import datetime

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
            name = chat.last_name + ' ' + chat.first_name
            user = cls.objects.create(user_id=chat.id, name=name)
        else:
            user = user[0]
        return user

class ScanDocument(me.Document):
    user = me.ReferenceField(User, reverse_delete_rule=me.DENY)
    date = me.DateTimeField(default=datetime.now())
    date_export_to_1c = me.DateTimeField()

    file_id = me.StringField(max_length=100)
    file_name = me.StringField(max_length=255)
    file_size = me.IntField()

    file_path = me.StringField(max_length=255)
    data_file = me.FileField()

    @classmethod
    def add_document(cls, user, document_message):
        document = cls.objects.create(user=user,
                                     file_id = document_message.file_id,
                                     file_name = document_message.file_name,
                                     file_size = document_message.file_size)
        return document


# for car in cars:
#     car_file = open(CAR_IMAGE, 'rb')
#     car_obj = Car.objects.create(title = car)
#     car_obj.photo.put(car_file, content_type='image/jpeg')

class Text(me.Document):
    START_MESSAGE = 'start_message',
    OTHER_MESSAGE = 'others_message',
    PHOTO_MESSAGE = 'photo_message',
    DOCUMENT_MESSAGE = 'document_message'

    TITLES_CONSTANT = (
        (START_MESSAGE, 'start message'),
        (OTHER_MESSAGE, 'others message'),
        (PHOTO_MESSAGE, 'photo message'),
        (DOCUMENT_MESSAGE, 'document message')
    )

    title = me.StringField(required=True, choices=TITLES_CONSTANT, unique=True)
    body = me.StringField(min_length=2, max_length=4096)

    @classmethod
    def get_body(cls, title_):
        _text = cls.objects(title=title_)
        if _text:
            return _text.body

        return 'Not text from  - ' + title_


    # text = 'Вітаємо. Ви підключилися до бота зберігання скана документів'

