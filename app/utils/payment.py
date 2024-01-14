import uuid

import requests


class PaymentProcessor:
    def __init__(self, card_number, expiry_date, cart_total):
        self.phone_number = None
        self.username = "test_merchant@gmail.com"
        self.password = "test_password"
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.cart_total = cart_total
        self.auth_token = self.get_access_token()
        self.card_token = self.create_card_token()
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
        auth_token = response.json().get('access_token')
        return auth_token

    def create_card_token(self):
        card_url = 'https://gateway-api-dev.globalpay.uz/cards/v1/card'
        card_data = {
            'cardNumber': self.card_number,
            'expiryDate': self.expiry_date
        }
        headers = {'Authorization': 'Bearer ' + self.auth_token, 'Content-Type': 'application/json'}
        card_response = requests.post(url=card_url, headers=headers, json=card_data)
        self.phone_number = card_response.json().get('smsNotificationNumber')
        print(card_response.json().get('smsNotificationNumber'))
        card_token = card_response.json().get('cardToken')
        return card_token

    def confirm_card(self, otp):
        otp_code = otp
        confirm_url = f'https://gateway-api-dev.globalpay.uz/cards/v1/card/confirm/{self.card_token}'
        confirm_data = {'code': 1}
        headers = {'Authorization': 'Bearer ' + self.auth_token, 'Content-Type': 'application/json'}
        confirm_response = requests.post(url=confirm_url, headers=headers, json=confirm_data)
        print(otp_code)
        print(type(otp_code))
        print(confirm_response.json())
        self.payment_id = self.init_payment()
        self.perform_payment()

    def init_payment(self):
        init_url = "https://gateway-api-dev.globalpay.uz/payments/v1/payment/init"
        init_data = {
            "externalId": f"{self.external_id}",
            "serviceId": 303,
            "paymentFields": [
                {"value": f"{self.cart_total}", "name": "amount"},
                {"value": "UZS", "name": "currency"}
            ]
        }
        headers = {'Authorization': 'Bearer ' + self.auth_token, 'Content-Type': 'application/json'}
        init_response = requests.post(url=init_url, headers=headers, json=init_data)
        payment_id = init_response.json().get('id')
        return payment_id

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
#
# payment = PaymentProcessor('9860090101219724', '2610')
# print(payment.auth_token)
# print('cart token' + payment.card_token)
# payment.confirm_card()
# print(payment.payment_id)
