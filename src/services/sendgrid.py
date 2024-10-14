from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Bcc, Cc, Content, Mail, Personalization, To


class SendgridClient:
    """
    Client for Sendgrid Mailing
    """

    def __init__(self, to_list: list = None, cc_list: list = [], bcc_list: list = [], data: dict = {}):
        self.message = Mail(
            from_email=f"{settings.PROJECT_NAME} <{settings.FROM_EMAIL}>",
        )

        personalization = Personalization()

        if to_list:
            for to in to_list:
                personalization.add_to(To(to))
        else:
            personalization.add_to(To(settings.FROM_EMAIL))

        for cc in cc_list:
            personalization.add_cc(Cc(cc))

        for bcc in bcc_list:
            personalization.add_bcc(Bcc(bcc))

        self.message.add_personalization(personalization)

        self.template_id = ""
        self.data = data

        self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)

    def send_email(self, subject, content):
        """
        Send plain text email
        """
        self.message.subject = subject
        self.message.content = Content("text/plain", content)

        if settings.SEND_EMAILS:
            return self.client.send(self.message)

    def send_dynamic_email(self, template_id=None, dynamic_template_data=None):
        """
        Send dynamic template email
        """
        if dynamic_template_data is not None and template_id is None:
            raise Exception("Cannot have dynamic_template_data without template_id")

        if template_id is not None:
            self.message.template_id = template_id
            self.message.dynamic_template_data = dynamic_template_data

        if settings.SEND_EMAILS:
            return self.client.send(self.message)
