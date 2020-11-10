from flask import Flask
from qr_reader.api import api_app
from qr_reader.bot import bot_instance

app = Flask(__name__)
app.register_blueprint(api_app)

if __name__ == '__main__':
    # app.run(host="172.30.222.182", debug=True)

    bot_instance.polling()

    # bot_instance.test_add()

