import random
import hashlib
import datetime

from django.conf import settings
from django.contrib.auth import get_user_model

from shareholder.models import Shareholder, Company, Position, Operator

User = get_user_model()

def _make_wordlist():

    words = [line.strip() for line in open('/usr/share/dict/american-english')]
    return words

def _make_user():

    words = _make_wordlist()
    hash_user = hashlib.sha1()
    hash_user.update(random.choice(words))
    username = hash_user.hexdigest()

    user = User.objects.create(
        is_active=True,
        first_name = random.choice(words),
        last_name = random.choice(words),
        username = username,
    )
    return user

class OperatorGenerator(object):

    def generate(self):
    
        word = random.choice(_make_wordlist())
        user = _make_user()

        company = Company.objects.create(
            name = '{} A.B.'.format(word),
            share_count = 3,
        )

        operator = Operator.objects.create(
            user=user,
            company=company,
        )

        return operator

class ShareholderGenerator(object):

    def generate(self, **kwargs):

        words = _make_wordlist()
        word = random.choice(_make_wordlist())
        user = _make_user()

        company = Company.objects.create(
            name = '{} A.B.'.format(word),
            share_count = 3,
        )

        shareholder = Shareholder.objects.create(
            user=user,
            number=random.choice(words)+"234543",
            company=company,
        )

        return shareholder

class PositionGenerator(object):

    def generate(self, **kwargs):
        if kwargs.get('shareholder'):
            buyer = kwargs.get('shareholder')
        else:
            buyer = ShareholderGenerator().generate()

        position = Position.objects.create(
            buyer=buyer,
            bought_at=datetime.datetime.now().date(),
            count = 3,
            value = 3,
        )

        return position
        
