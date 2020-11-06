import requests


with open('./IMG/test.jpg', 'rb') as f1:
    files = [
        ('profile', f1)
    ]
    requests.post('http://172.30.222.182:5000/qr', files=files)