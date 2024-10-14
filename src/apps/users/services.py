from django.conf import settings
from sentry_sdk import capture_exception

from services.sendgrid import SendgridClient


def send_initial_register_password_email(user, url):
    try:
        sendgrid = SendgridClient(
            to_list=[user.email],
        )
        sendgrid.send_dynamic_email(
            template_id=settings.SENDGRID_INITIAL_RESET_PASSWORD_TEMPLATE,
            dynamic_template_data={
                "project": settings.PROJECT_NAME,
                "url": url,
            },
        )
    except Exception as e:
        capture_exception(e)


def send_password_reset_email(user, url):
    try:
        sendgrid = SendgridClient(
            to_list=[user.email],
        )
        sendgrid.send_dynamic_email(
            template_id=settings.SENDGRID_RESET_PASSWORD_TEMPLATE,
            dynamic_template_data={
                "url": url,
            },
        )
    except Exception as e:
        capture_exception(e)
