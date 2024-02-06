import requests

url = 'https://notify.eskiz.uz/api/auth/login'
data = {
    'email': 'bcloudintelekt@gmail.com',
    'password': 'ddMFQPXTfQRuhj8nmNSyfLv6mniuSpBHxGj3ZEY5',
}

response = requests.post(url, data=data)

TOKEN = response.json()['data']['token']