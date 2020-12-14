import requests


with open('./IMG/test.jpg', 'rb') as f1:
    files = [
        ('file', f1)
    ]
    requests.post('http://172.30.222.182:5000/rotate_image', files=files)