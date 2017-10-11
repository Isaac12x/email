from sys import argv
import requests
import json

script, email = argv


def check_for_disposable_emails(email):
    url_to_check = 'https://www.validator.pizza/email/%s' % (email)

    try:
        response = requests.get(url_to_check)
        data = json.loads(response.text)
        print(data)
        if response.status_code is 200:
            if data['mx'] is not True & data['disposable'] is not False:
                return True
    except:
        return False
