import random
import hashlib

from django.conf import settings
from django.contrib.auth import get_user_model

from shareholder.models import Shareholder, Company

User = get_user_model()

class ShareholderGenerator(object):

    def generate(self, **kwargs):

        hash_user = hashlib.sha1()

        words = [line.strip() for line in open('/usr/share/dict/american-english')]
        word = random.choice(words)

        hash_user.update(random.choice(words))
        username = hash_user.hexdigest()

        company = Company.objects.create(
            name = '{} A.B.'.format(word),
        )

        user = User.objects.create(
            is_active=True,
            first_name = random.choice(words),
            last_name = random.choice(words),
            username = username,
        )

        shareholder = Shareholder.objects.create(
            user=user,
            number=random.choice(words)+"234543",
            company=company,
        )

        return shareholder
