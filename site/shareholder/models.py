import os
import time

from decimal import Decimal

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext as _


class Country(models.Model):
    """Model for countries"""
    iso_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=45, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name", "iso_code"]


class Company(models.Model):

    name = models.CharField(max_length=255)
    share_count = models.PositiveIntegerField(blank=True, null=True)
    country = models.ForeignKey(
        Country, null=True, blank=False, help_text=_("Headquarter location"))

    def __str__(self):
        return u"{}".format(self.name)

    def shareholder_count(self):
        """ total count of active Shareholders """
        return Position.objects.filter(
            buyer__company=self, seller__isnull=True).count()

    def get_active_shareholders(self):
        """ returns list of all active shareholders """
        shareholder_list = []
        for shareholder in self.shareholder_set.all().order_by('number'):
            if shareholder.share_count() > 0:
                shareholder_list.append(shareholder)
        return shareholder_list


class UserProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, blank=True, null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255, blank=False, null=True)
    postal_code = models.CharField(max_length=255)
    country = models.ForeignKey(Country, blank=False)

    company_name = models.CharField(max_length=255, blank=False, null=True)
    birthday = models.DateField()

    def __unicode__(self):
        return "%s, %s %s" % (self.city, self.province,
                              str(self.country))

    class Meta:
        verbose_name_plural = "Addresses"


class Shareholder(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company')
    number = models.CharField(max_length=255)

    def __str__(self):
        return u"{} {} ({})".format(
            self.user.first_name, self.user.last_name, self.number)

    def share_percent(self):
        """ returns percentage of shares owned compared to corps
        total shares """
        total = self.company.share_count
        count = sum(self.buyer.all().values_list('count', flat=True)) - \
            sum(self.seller.all().values_list('count', flat=True))
        if total:
            return "{:.2f}".format(count / float(total) * 100)
        return False

    def share_count(self):
        """ total count of shares for shareholder  """
        return sum(self.buyer.all().values_list('count', flat=True)) - \
            sum(self.seller.all().values_list('count', flat=True))

    def share_value(self):
        """ calculate the total values of all shares for this shareholder """
        share_count = self.share_count()
        if share_count == 0:
            return 0

        # last payed price
        position = Position.objects.filter(buyer__company=self.company).latest(
            'bought_at')
        return share_count * position.value

    def validate_gafi(self):
        """ returns dict with indication if all data is correct to match
        swiss fatf gafi regulations """
        result = {"is_valid": True, "errors": []}

        # applies only for swiss corps
        if (
            not self.company.country or
            self.company.country.iso_code.lower() != 'ch'
        ):
            return result

        # missing profile leads to global warning
        if not hasattr(self.user, 'userprofile'):
            result['is_valid'] = False
            result['errors'].append(_("Missing all data required for #GAFI."))
            return result

        if not (self.user.first_name and self.user.last_name) or not \
                self.user.userprofile.company_name:
            result['is_valid'] = False
            result['errors'].append(_(
                'Shareholder first name, last name or company name missing.'))

        if not self.user.userprofile.birthday:
            result['is_valid'] = False
            result['errors'].append(_('Shareholder birthday missing.'))

        if not self.user.userprofile.country:
            result['is_valid'] = False
            result['errors'].append(_('Shareholder origin/country missing.'))

        if not self.user.userprofile.city or not self.user.userprofile.postal_code or not \
                self.user.userprofile.street:
            result['is_valid'] = False
            result['errors'].append(_(
                'Shareholder address or address details missing.'))

        return result


class Operator(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company')
    share_count = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return u"{} {}".format(self.user.first_name, self.user.last_name)


class Security(models.Model):
    SECURITY_TITLES = (
        ('P', 'Preferred Stock'),
        ('C', 'Common Stock'),
        # ('O', 'Option'),
        # ('W', 'Warrant'),
        # ('V', 'Convertible Instrument'),
    )
    title = models.CharField(max_length=1, choices=SECURITY_TITLES)
    company = models.ForeignKey(Company)
    count = models.PositiveIntegerField()

    def __str__(self):
        return u"{}".format(self.get_title_display())


class Position(models.Model):

    buyer = models.ForeignKey('Shareholder', related_name="buyer")
    seller = models.ForeignKey('Shareholder', blank=True, null=True,
                               related_name="seller")
    security = models.ForeignKey(Security)
    count = models.PositiveIntegerField()
    bought_at = models.DateField()
    value = models.DecimalField(max_digits=8, decimal_places=4, blank=True,
                                null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def get_option_plan_upload_path(instance, filename):
    return os.path.join(
        "private", "optionplan", "%d" % instance.id, filename)


class OptionPlan(models.Model):
    """ Approved chunk of option (approved by board) """
    company = models.ForeignKey('Company')
    board_approved_at = models.DateField()
    title = models.CharField(max_length=255)
    security = models.ForeignKey('Security')
    exercise_price = models.DecimalField(
        max_digits=8, decimal_places=4,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))]
        )
    count = models.PositiveIntegerField(
        help_text=_("Number of shares approved"))
    comment = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(
        blank=True, null=True,
        upload_to=get_option_plan_upload_path,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"{}".format(self.title)

    def generate_pdf_file_preview(self):
        """ generates preview png in same place """
        from wand.image import Image
        # Converting first page into JPG
        with Image(filename=self.pdf_file.file.name+"[0]") as img:
            width, height = img.size
            # img.resize(300, int(300/float(width)*float(height)))
            img.save(filename=self.pdf_file_preview_path())

    def pdf_file_preview_path(self):
        if not self.pdf_file:
            return None
        s = self.pdf_file.file.name.split(".")
        s = s[:-1]
        s.extend(['png'])
        return ".".join(s)

    def pdf_file_preview_url(self):
        if not self.pdf_file:
            return None
        # needs timestamp to trigger reload
        return "/optionsplan/{}/download/img/?t={}".format(self.pk, time.time())

    def pdf_file_url(self):
        if not self.pdf_file:
            return None
        return "/optionsplan/{}/download/pdf/".format(self.pk)


class OptionTransaction(models.Model):
    """ Transfer of options from someone to anyone """
    bought_at = models.DateField()
    buyer = models.ForeignKey('Shareholder', related_name="option_buyer")
    option_plan = models.ForeignKey('OptionPlan')
    count = models.PositiveIntegerField()
    seller = models.ForeignKey('Shareholder', blank=True, null=True,
                               related_name="option_seller")
    vesting_months = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# --------- SIGNALS ----------
# must be inside a file which is imported by django on startup

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
