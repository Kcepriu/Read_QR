import time
from flask import Flask
from qr_reader.api import api_app
from qr_reader.bot import bot_instance
from qr_reader.bot import bot_app
from qr_reader.bot.config import WEBHOOK_URL

app = Flask(__name__)
app.register_blueprint(api_app)
app.register_blueprint(bot_app)

if __name__ == '__main__':
    #app.run(host="172.30.222.182", debug=True)

    # bot_instance.polling()

    # bot_instance.test_add()

    bot_instance.remove_webhook()
    time.sleep(2)
    a = bot_instance.set_webhook(
        url=WEBHOOK_URL,
        certificate=open('webhook_cert.pem', 'r')
    )

    app.run(host="172.40.99.100")


