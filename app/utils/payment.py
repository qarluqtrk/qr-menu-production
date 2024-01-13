import uuid

import requests


class PaymentProcessor:
    def __init__(self, username, password, card_number, expiry_date):
        self.username = username
        self.password = password
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.auth_token = None
        self.card_token = None
        self.external_id = str(uuid.uuid4())
        self.payment_id = None

    def get_access_token(self):
        url = 'https://sso-selectel-dev.globalpay.uz/realms/globalpay/protocol/openid-connect/token'
        data = {
            'grant_type': 'password',
            'client_id': 'cards',
            'client_secret': 'CCcmoAt8cI3NEY9HDN64SQD4qR8DanMh',
            'username': self.username,
            'password': self.password,
            'scope': 'openid'
        }
        response = requests.post(url, data=data)
        self.auth_token = response.json().get('access_token')

    def create_card_token(self):
        card_url = 'https://gateway-api-dev.globalpay.uz/cards/v1/card'
        card_data = {
            'cardNumber': self.card_number,
            'expiryDate': self.expiry_date
        }
        headers = {'Authorization': 'Bearer ' + self.auth_token, 'Content-Type': 'application/json'}
        card_response = requests.post(url=card_url, headers=headers, json=card_data)
        self.card_token = card_response.json().get('cardToken')
        print(f"CardToken : {self.card_token}")

    def confirm_card(self):
        otp_code = input('Enter OTP: ')
        confirm_url = f'https://gateway-api-dev.globalpay.uz/cards/v1/card/confirm/{self.card_token}'
        confirm_data = {'code': otp_code}
        headers = {'Authorization': 'Bearer ' + self.auth_token, 'Content-Type': 'application/json'}
        confirm_response = requests.post(url=confirm_url, headers=headers, json=confirm_data)

    def init_payment(self):
        init_url = "https://gateway-api-dev.globalpay.uz/payments/v1/payment/init"
        init_data = {
            "externalId": f"{self.external_id}",
            "serviceId": 303,
            "paymentFields": [
                {"value": "100000", "name": "amount"},
                {"value": "UZS", "name": "currency"}
            ]
        }
        headers = {'Authorization': 'Bearer ' + self.auth_token, 'Content-Type': 'application/json'}
        init_response = requests.post(url=init_url, headers=headers, json=init_data)
        self.payment_id = init_response.json().get('id')
        print(f"PaymentID : {self.payment_id}")

    def perform_payment(self):
        perform_url = "https://gateway-api-dev.globalpay.uz/payments/v1/payment/perform"
        perform_data = {
            "externalId": f"{self.external_id}",
            "id": self.payment_id,
            "cardToken": self.card_token
        }
        headers = {'Authorization': 'Bearer ' + self.auth_token, 'Content-Type': 'application/json'}
        perform_response = requests.post(url=perform_url, headers=headers, json=perform_data)
        print(perform_response.json())


# Example usage:
