from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Returns comma separated email list for newsletters'

    def handle(self, *args, **options):

        self.stdout.write(
            ", ".join([user.email for user in User.objects.exclude(email='')])
        )
