from django.conf import settings
from pusher import Pusher


class PusherClient:
    """
    Client for Pusher WebSockets
    """

    def __init__(self):
        self.client = Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET,
            cluster="us2",
            ssl=True,
        )

    def trigger(self, channel: str, event: str, data: dict):
        """
        Trigger pusher event
        """
        self.client.trigger(channel, event, data)
