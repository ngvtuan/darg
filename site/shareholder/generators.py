import random
import hashlib
import datetime

from django.contrib.auth import get_user_model
from django.utils.text import slugify

from shareholder.models import Shareholder, Company, Position, Operator, \
    UserProfile, Country, Security
from utils.user import make_username

User = get_user_model()

DEFAULT_TEST_DATA = {
    'password': 'test',
    'username': 'testusername',
    'date': '1.1.2016',
    'title': '2016 OptionsPlan',
    'exercise_price': '2.05',
    'share_count': '156',
    'comment': '2345',
    'security': 'Preferred Stock',
    'count': '2222',
    'vesting_period': 3,
}


def _make_wordlist():

    words = [line.strip() for line in open('/usr/share/dict/american-english')]
    return words


def _make_user():

    words = _make_wordlist()
    hash_user = hashlib.sha1()
    hash_user.update(random.choice(words))
    username = hash_user.hexdigest()[0:25]
    email = "{}@{}".format(username, 'example.com')

    user = User.objects.create(
        is_active=True,
        first_name=random.choice(words),
        last_name=random.choice(words),
        username=username,
        email=email,
    )

    country, created = Country.objects.get_or_create(
        iso_code="de", defaults={"name": "Germany", "iso_code": "de"})

    # reload user to get the userprofile created by signal too
    user = User.objects.get(id=user.id)
    UserProfile.objects.filter(user=user).update(**dict(
        country=country,
        street="Some Street",
        city="SomeCity",
        province="Some Province",
        postal_code="12345",
        birthday=datetime.datetime.now(),
        company_name="SomeCorp"
        )
    )

    user.set_password(DEFAULT_TEST_DATA.get('password'))
    user.save()

    return user


class CompanyGenerator(object):

    def generate(self, **kwargs):

        word = random.choice(_make_wordlist())
        name = kwargs.get('name') or '{} A.B.'.format(word)
        share_count = kwargs.get('share_count') or 3
        country = kwargs.get('country') or CountryGenerator().generate()

        kwargs2 = {
            "name": name,
            "share_count": share_count,
            "country": country,
        }

        company = Company.objects.create(**kwargs2)

        return company


class SecurityGenerator(object):

    def generate(self, **kwargs):
        company = kwargs.get('company', CompanyGenerator().generate())
        s1 = Security.objects.create(title='P', company=company, count=1)

        return s1


class CountryGenerator(object):

    def generate(self):
        country, created = Country.objects.get_or_create(
            iso_code="de", defaults={"name": "Germany", "iso_code": "de"})
        return country


class UserGenerator(object):
    """ generate plain user """

    def generate(self):
        user = _make_user()

        return user


class OperatorGenerator(object):

    def generate(self, **kwargs):

        word = random.choice(_make_wordlist())
        user = kwargs.get("user") or _make_user()

        company = kwargs.get("company") or \
            Company.objects.create(
                name='{} A.B.'.format(word),
                share_count=3,
                country=CountryGenerator().generate()
            )

        operator = Operator.objects.create(
            user=user,
            company=company,
        )

        return operator


class ShareholderGenerator(object):

    def generate(self, **kwargs):

        words = _make_wordlist()

        number = kwargs.get('number') or random.choice(words)+"234543"
        user = kwargs.get('user') or _make_user()
        company = kwargs.get('company') or CompanyGenerator().generate()

        shareholder = Shareholder.objects.create(
            user=user,
            number=number,
            company=company,
        )

        return shareholder


class CompanyShareholderGenerator(object):

    def generate(self, **kwargs):

        company = kwargs.get('company') or CompanyGenerator().generate()
        company_shareholder_created_at = kwargs.get('company_shareholder_created_at') or \
            datetime.datetime.now()
        companyuser = User.objects.create(
            username=make_username('Company', 'itself', company.name),
            first_name='Company', last_name='itself',
            email='info@{}-company-itself.com'.format(slugify(company.name))
        )
        shareholder = Shareholder.objects.create(
            user=companyuser,
            company=company,
            number='0')

        pos_kwargs = kwargs.copy()
        pos_kwargs.update({
            'buyer': shareholder,
            'count': company.share_count,
            'bought_at': company_shareholder_created_at
        })

        PositionGenerator().generate(**pos_kwargs)

        return shareholder


class PositionGenerator(object):

    def generate(self, **kwargs):
        company = kwargs.get('company') \
            or kwargs.get('buyer').company \
            or kwargs.get('seller').company \
            or kwargs.get('security').company \
            or CompanyGenerator
        buyer = kwargs.get('buyer') or ShareholderGenerator().generate(
            company=company)
        seller = kwargs.get('seller') or None
        count = kwargs.get('count') or 3
        value = kwargs.get('value') or 2
        security = kwargs.get('security') or SecurityGenerator().generate(
            company=company)
        bought_at = kwargs.get('bought_at') or datetime.datetime.now().date()

        kwargs2 = {
            "buyer": buyer,
            "bought_at": bought_at,
            "count": count,
            "value": value,
            "security": security,
        }
        if seller:
            kwargs2.update({"seller": seller})

        position = Position.objects.create(**kwargs2)

        return position


class TwoInitialSecuritiesGenerator(object):

    def generate(self, **kwargs):
        if kwargs.get('company'):
            company = kwargs.get('company')
        else:
            company = CompanyGenerator().generate()
        s1 = Security.objects.create(title='P', company=company, count=1)
        s2 = Security.objects.create(title='C', company=company, count=2)

        return (s1, s2)


class ComplexShareholderConstellationGenerator(object):

    def generate(self, **kwargs):

        company = kwargs.get('company') or CompanyGenerator().generate()

        # intial securities
        s1, s2 = TwoInitialSecuritiesGenerator().generate(company=company)

        # initial company shareholder
        company_shareholder_created_at = kwargs.get('company_shareholder_created_at') or\
            datetime.datetime.now()
        cs = CompanyShareholderGenerator().generate(
            company=company, security=s1,
            company_shareholder_created_at=company_shareholder_created_at)

        # random shareholder generation
        shareholders = [cs]
        # initial share seeding
        for i in range(0, 10):
            shareholders.append(PositionGenerator().generate(
                company=company, security=s1, seller=cs).buyer)

        # two shareholders sold again
        shareholders.append(
            PositionGenerator().generate(
                company=company,
                seller=shareholders[3],
                security=s1).buyer)
        shareholders.append(
            PositionGenerator().generate(
                company=company,
                seller=shareholders[6],
                security=s1).buyer)

        return shareholders, s1
