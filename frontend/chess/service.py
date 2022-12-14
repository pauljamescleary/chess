
import requests
from requests.auth import HTTPBasicAuth

class InvalidLoginException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class ChessService:

    def __init__(self, base_url):
        self.base_url = base_url
        self.basic_auth = None

    def signup(self, email, password):
        payload = { 'email': email, 'password': password}
        print(f"Calling signup with email {email} and password {password}")
        response = requests.post('http://127.0.0.1:5000/users', json=payload)
        if response.status_code != 200:
            print(response.text)
            raise RuntimeError('Unexpected error during signup')
        else:
            self.basic_auth = HTTPBasicAuth(email, password)


    def login(self, email, password):
        print(f"*** LOGGING IN WITH EMAIL {email} AND PASSWORD {password}")
        ba = HTTPBasicAuth(email, password)
        response = requests.get('http://127.0.0.1:5000/user', auth=ba)
        if response.status_code != 200:
            print(f"RESPONSE STATUS: {response.status_code}")
            print(response.text)
            raise InvalidLoginException
        else:
            self.basic_auth = ba

    def save_score(self, score, level):
        payload = { 'score': score, 'level': level}
        response = requests.post('http://127.0.0.1:5000/scores', auth=self.basic_auth, data=payload)

        if response.status_code != 200:
            print(response.text)
            raise RuntimeError('Unexpected error saving score')

    def get_high_score(self):
        response = requests.get('http://127.0.0.1:5000/scores/top', auth=self.basic_auth)
        if response.status_code != 200:
            print(response.text)
            raise RuntimeError('Unexpected error getting high score')
        else:
            return response.json()

