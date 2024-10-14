from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):
    help = "Create Test Superuser"

    def handle(self, *args, **options):
        try:
            User.objects.create_superuser(email="dev@comuna18.com", password="7h8j9k0l")
            print("Superuser created!")
        except Exception as e:
            print(e)
