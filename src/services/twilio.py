from django.conf import settings
from twilio.rest import Client


class TwilioService:
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    def __init__(self):
        self.client = Client(self.account_sid, self.auth_token)

    def send_whatsapp(self, conversation_id: str, content: str) -> None:
        self.client.conversations.v1.conversations(conversation_id).messages.create(body=content)

    def send_sms(self, phone: str, content: str) -> None:
        self.client.messages.create(from_=settings.TWILIO_SMS_NUMBER, to=f"+{phone}", body=content)
