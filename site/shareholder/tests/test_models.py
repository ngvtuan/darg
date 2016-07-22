#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal

from django.core import mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.test import TestCase, TransactionTestCase
from django.test.client import Client, RequestFactory

from shareholder.generators import (CompanyGenerator,
                                    ComplexPositionsWithSegmentsGenerator,
                                    ComplexShareholderConstellationGenerator,
                                    OperatorGenerator, PositionGenerator,
                                    SecurityGenerator, ShareholderGenerator,
                                    UserGenerator)
from shareholder.models import Country, Position, Security, Shareholder


# --- MODEL TESTS
class CountryTestCase(TestCase):

    def test_model(self):

        Country.objects.create(iso_code='de', name="Germany")

        qs = Country.objects.all()
        country = qs[0]

        self.assertEqual(qs.count(), 1)
        self.assertEqual(country.iso_code, 'de')
        self.assertEqual(country.name, 'Germany')


class PositionTestCase(TransactionTestCase):

    def test_split_shares(self):
        """ share split leaves value, percent unchanged but
        increases share count per shareholder
        """
        # test data
        company = CompanyGenerator().generate(share_count=1000)
        OperatorGenerator().generate(company=company)
        shareholders, security = ComplexShareholderConstellationGenerator()\
            .generate(company=company)

        data = {
            'execute_at': datetime.datetime.now(),
            'dividend': 3,
            'divisor': 7,
            'comment': "Some random comment",
            'security': security,
        }
        multiplier = float(data['divisor']) / float(data['dividend'])
        company_share_count = company.share_count

        # record initial shareholder asset status
        assets = {}
        for shareholder in shareholders:
            assets.update({
                shareholder.pk: {
                    'count': shareholder.share_count(),
                    'value': shareholder.share_value(),
                    'percent': shareholder.share_percent()
                }
            })

        # run
        company.split_shares(data)

        # asserts by checking overall shareholder situation
        # means each shareholder should have now more shares but some
        # overall stock value

        for shareholder in shareholders:
            self.assertEqual(
                shareholder.share_count(),
                round(assets[shareholder.pk]['count'] * multiplier)
            )
            self.assertEqual(
                round(shareholder.share_value()),
                assets[shareholder.pk]['value']
            )
            self.assertEqual(
                round(float(shareholder.share_percent()), 2),
                float(assets[shareholder.pk]['percent'])
            )

        self.assertEqual(
            company.share_count,
            round(company_share_count * multiplier))

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(
            mail.outbox[0].subject,
            u"Ihre Liste gespaltener Aktienanrechte f\xfcr das Unternehmen "
            u"'{}'".format(company.name)
        )

    def test_split_shares_in_past(self):
        """
        we are splitting shares at some point in the past
        even with newer transactions entered
        approach: split in the very past and check that nothing was changed
        """
        # test data
        company = CompanyGenerator().generate(
            share_count=1000,
        )
        OperatorGenerator().generate(company=company)
        shareholders, security = ComplexShareholderConstellationGenerator()\
            .generate(
                company=company,
                company_shareholder_created_at='2013-1-1'
            )

        data = {
            'execute_at': datetime.datetime(2014, 1, 1),
            'dividend': 3,
            'divisor': 7,
            'comment': "Some random comment",
            'security': security,
        }
        company_share_count = company.share_count

        # record initial shareholder asset status
        assets = {}
        d = datetime.datetime(2014, 1, 1)
        for shareholder in shareholders:
            assets.update({
                shareholder.pk: {
                    'count': shareholder.share_count(date=d),
                    'value': shareholder.share_value(date=d),
                    'percent': shareholder.share_percent(date=d)
                }
            })
        pcount = Position.objects.count()

        # run
        company.split_shares(data)

        # asserts by checking overall shareholder situation
        # means each shareholder should have now more shares but some
        # overall stock value
        cs = shareholders[0]
        mx = float(data['divisor']) / float(data['dividend'])
        for shareholder in shareholders:
            m = 1
            if shareholder.pk == cs.pk:
                m = mx
            self.assertEqual(
                shareholder.share_count(date=d),
                round(assets[shareholder.pk]['count'] * m)
            )

            # self.assertEqual(
            #     round(shareholder.share_value(date=d)),
            #     assets[shareholder.pk]['value']
            # )
            # self.assertEqual(
            #     round(float(shareholder.share_percent(date=d)), 2),
            #     float(assets[shareholder.pk]['percent'])
            # )

        self.assertEqual(
            company.share_count,
            round(company_share_count * mx))

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(
            mail.outbox[0].subject,
            u"Ihre Liste gespaltener Aktienanrechte f\xfcr das Unternehmen "
            u"'{}'".format(company.name)
        )
        # only one new pos as no shares were basically existing as we
        # split even before company creates their first shares
        self.assertEqual(pcount + 2, Position.objects.count())

    def test_watter_split_61(self):
        """
        issue shares multiple times, sell some of them then do a split. see #61
        """
        company = CompanyGenerator().generate(share_count=10000000)
        sc = ShareholderGenerator().generate(company=company)  # aka Company
        s1 = ShareholderGenerator().generate(company=company)  # aka W
        s2 = ShareholderGenerator().generate(company=company)  # aka S
        OperatorGenerator().generate(company=company)
        security = SecurityGenerator().generate(company=company)
        now = datetime.datetime.now()
        PositionGenerator().generate(
            buyer=s2, seller=sc, count=10000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=11)
        )  # initial seed

        p1 = PositionGenerator().generate(
            buyer=s1, seller=sc, count=187, value=100, security=security,
            bought_at=now-datetime.timedelta(days=10)
            )
        p2 = PositionGenerator().generate(
            buyer=s1, seller=sc, count=398, value=100, security=security,
            bought_at=now-datetime.timedelta(days=9)
            )
        PositionGenerator().generate(
            buyer=s2, seller=s1, count=80, value=100, security=security,
            bought_at=now-datetime.timedelta(days=8)
            )
        PositionGenerator().generate(
            buyer=s2, seller=s1, count=437, value=100, security=security,
            bought_at=now-datetime.timedelta(days=7)
            )
        PositionGenerator().generate(
            buyer=s1, seller=sc, count=837, value=100, security=security,
            bought_at=now-datetime.timedelta(days=6)
            )
        PositionGenerator().generate(
            buyer=s1, seller=sc, count=68, value=100, security=security,
            bought_at=now-datetime.timedelta(days=5)
            )

        split_data = {
            'execute_at': now - datetime.timedelta(days=4),
            'dividend': 1,
            'divisor': 100,
            'comment': "MEGA SPLIT",
            'security': security,
        }
        company.split_shares(split_data)

        PositionGenerator().generate(
            buyer=s1, seller=sc, count=3350, value=100, security=security,
            bought_at=now-datetime.timedelta(days=3)
            )

        self.assertEqual(s1.share_count(), 100650)
        positions = Position.objects.filter(comment__contains="split").filter(
            Q(buyer=s1) | Q(seller=s1)
        )
        self.assertEqual(positions.count(), 2)
        p1 = positions[0]
        p2 = positions[1]
        self.assertEqual(p1.count, 973)
        self.assertEqual(p1.buyer, sc)
        self.assertEqual(p1.seller, s1)
        self.assertEqual(p2.count, 97300)
        self.assertEqual(p2.seller, sc)
        self.assertEqual(p2.buyer, s1)


class UserProfileTestCase(TestCase):

    def test_model(self):

        user = UserGenerator().generate()
        profile = user.userprofile

        self.assertEqual(profile.country.iso_code, 'de')
        self.assertEqual(profile.country.name, 'Germany')
        self.assertEqual(profile.province, 'Some Province')


class ShareholderTestCase(TestCase):

    fixtures = ['initial.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_index(self):

        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Das Akt" in response.content)

    def test_validate_gafi(self):
        """ test the gafi validation """

        # --- invalid street
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        shareholder.user.userprofile.street = ''
        shareholder.user.userprofile.save()

        self.assertFalse(shareholder.validate_gafi()['is_valid'])

        # --- invalid company name
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        shareholder.user.userprofile.company_name = None
        shareholder.user.userprofile.save()

        self.assertFalse(shareholder.validate_gafi()['is_valid'])

        # --- valid data
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        self.assertTrue(shareholder.validate_gafi()['is_valid'])

    def test_validate_gafi_with_missing_userprofile(self):
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        profile = shareholder.user.userprofile
        profile.delete()

        shareholder = Shareholder.objects.get(id=shareholder.id)
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        self.assertFalse(hasattr(shareholder.user, 'userprofile'))
        self.assertFalse(shareholder.validate_gafi()['is_valid'])

    def test_shareholder_detail(self):
        """ test detail view for shareholder """

        shareholder = ShareholderGenerator().generate()

        response = self.client.login(
            username=shareholder.user.username, password="test")
        self.assertTrue(response)

        response = self.client.get(
            reverse("shareholder", args=(shareholder.id,)))

        self.assertEqual(response.status_code, 200)

    def test_share_percent(self):
        """
        proper share percent math
        """
        company = CompanyGenerator().generate(share_count=1000000)
        security = SecurityGenerator().generate(company=company)
        sc = ShareholderGenerator().generate(company=company)
        s1 = ShareholderGenerator().generate(company=company)
        s2 = ShareholderGenerator().generate(company=company)
        s3 = ShareholderGenerator().generate(company=company)
        now = datetime.datetime.now()

        PositionGenerator().generate(
            buyer=sc, count=1000000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=11)
            )
        PositionGenerator().generate(
            buyer=s1, seller=sc, count=500000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=10)
            )
        PositionGenerator().generate(
            buyer=s2, seller=sc, count=5000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=9)
            )
        PositionGenerator().generate(
            buyer=s3, seller=sc, count=50, value=100, security=security,
            bought_at=now-datetime.timedelta(days=8)
            )

        self.assertEqual(s1.share_percent(), '99.00')
        self.assertEqual(s2.share_percent(), '0.99')
        self.assertEqual(s3.share_percent(), '0.01')

        PositionGenerator().generate(
            buyer=s2, seller=s1, count=250000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=7)
            )

        self.assertEqual(s1.share_percent(), '49.50')

    def test_share_value(self):
        """
        share value is last trated price
        """
        company = CompanyGenerator().generate(share_count=1000000)
        security = SecurityGenerator().generate(company=company)
        sc = ShareholderGenerator().generate(company=company)
        s1 = ShareholderGenerator().generate(company=company)
        now = datetime.datetime.now()

        PositionGenerator().generate(
            buyer=sc, count=1000000, value=1, security=security,
            bought_at=now-datetime.timedelta(days=11)
            )
        p = PositionGenerator().generate(
            buyer=s1, seller=sc, count=500000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=10)
            )
        p.value = None
        p.save()

        self.assertEqual(s1.share_value(), Decimal('500000.0000'))

    def test_owns_segments(self):
        """
        check if shareholder owns this list of segments. returns false on first
        fail
        """
        positions, shs = ComplexPositionsWithSegmentsGenerator().generate()
        segments = [1000, 1050, 1666, u'1103-1105']

        self.assertEqual(
            shs[1].owns_segments(segments, positions[0].security),
            (True, [], [u'1000-1200', 1666]))

        segments = [1000, 1050, 1666, 1667]

        self.assertEqual(
            shs[1].owns_segments(segments, positions[0].security),
            (False, [1667], [u'1000-1200', 1666]))

    def test_current_segments(self):
        """
        get shareholders list of segments owned
        """
        positions, shs = ComplexPositionsWithSegmentsGenerator().generate()

        self.assertEqual(shs[1].current_segments(positions[0].security), [u'1000-1200', 1666])


class SecurityTestCase(TestCase):

    def test_fields(self):
        security = SecurityGenerator().generate()

        self.assertTrue(hasattr(security, 'track_numbers'))
        self.assertTrue(hasattr(security, 'face_value'))
        self.assertTrue(hasattr(security, 'number_segments'))

        segments = [1, 2, 3, '4-6']
        security.number_segments = segments
        security.save()

        # refresh from db
        s = Security.objects.get(id=security.id)
        self.assertEqual(s.number_segments, segments)

    def test_count_in_segments(self):
        """
        count shares in segments
        """
        security = SecurityGenerator().generate()

        segments = '1, 3,4, 99-1000'
        count = security.count_in_segments(segments)
        self.assertEqual(count, 905)

        segments = [1, 3, 4, 5, u'99-1000']
        count = security.count_in_segments(segments)
        self.assertEqual(count, 906)
