import os
import time
import datetime
import logging
import math

from decimal import Decimal

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

logger = logging.getLogger(__name__)


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
    founded_at = models.DateField(
        _('Foundation date of the company'),
        null=True, blank=False)
    provisioned_capital = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return u"{}".format(self.name)

    def __unicode__(self):
        return u"{}".format(self.name)

    def _send_partial_share_rights_email(self, partials):
        """ send email with partial share after split list """
        operators = self.get_operators().values_list('user__email', flat=True)
        subject = _(
            "Your list of partials for the share split for "
            "company '{}'").format(self.name)
        message = _(
            "Dear Operator,\n\n"
            "Your share split has been successful. Please find the list of "
            "partial shares below:\n\n"
        )

        if len(partials) > 0:
            for id, part in partials.iteritems():
                s = Shareholder.objects.get(id=id)
                message = message + _("{}{}({}): {} shares\n").format(
                    s.user.first_name,
                    s.user.last_name,
                    s.user.email,
                    part,
                )
        else:
            message = message + _("--- No partial shares during split --- \n")

        message = message + _(
            "\nThese shareholders are eligible to either "
            "sell their partial shares or get compensated.\n\n"
            "Please handle them accordingly and update the share "
            "register.\n\n"
            "Your Share Register Team"
            )
        send_mail(
            subject, message, settings.SERVER_EMAIL,
            operators, fail_silently=False)
        logger.info(
            'split partials mail sent to operators: {}'.format(
                operators))

    # --- GETTER
    def shareholder_count(self):
        """ total count of active Shareholders """
        return Position.objects.filter(
            buyer__company=self, seller__isnull=True).count()

    def get_active_shareholders(self, date=None):
        """ returns list of all active shareholders """
        shareholder_list = []
        for shareholder in self.shareholder_set.all().order_by('number'):
            if shareholder.share_count(date=date) > 0:
                shareholder_list.append(shareholder)

        return shareholder_list

    def get_company_shareholder(self):
        return self.shareholder_set.earliest('id')

    def get_operators(self):
        return self.operator_set.all().distinct()

    def get_provisioned_capital(self):
        """ its libiertes or eingelegtes capital. means on company
        foundation the capital is provisioned by the shareholders.
        e.g. if company was founded with 1m chf equity, owners might have
        provided only 200k. this value here would then be 200k """

        return self.provisioned_capital

    def get_total_capital(self):
        """ returns the total monetary value of the companies
        capital (Nennkapital) by getting all share creation positions (inital
        and increases) and sum up count*val
        """
        cap_creating_positions = Position.objects.filter(
            buyer__company=self, seller__isnull=True)
        val = 0
        for position in cap_creating_positions:
            val += position.count * position.value

        cap_destroying_positions = Position.objects.filter(
            seller__company=self, buyer__isnull=True)

        for position in cap_destroying_positions:
            val -= position.count * position.value

        return val

    # --- LOGIC
    def split_shares(self, data):
        """ split all existing positions """
        execute_at = data['execute_at']
        dividend = float(data['dividend'])
        divisor = float(data['divisor'])
        security = data['security']

        # get all active shareholder on day 'execute_at'
        shareholders = self.get_active_shareholders(date=execute_at)
        company_shareholder = self.get_company_shareholder()

        # create return transactions to return old assets to company
        # create transaction to hand out new assets to shareholders with
        # new count
        value = float(company_shareholder.last_traded_share_price(
            date=execute_at, security=security))
        partials = {}
        for shareholder in shareholders:
            count = shareholder.share_count(
                execute_at, security)
            kwargs1 = {
                'buyer': company_shareholder,
                'seller': shareholder,
                'count': count,
                'value': value,
                'security': security,
                'bought_at': execute_at,
                'is_split': True,
                'comment': _('Share split of {} on {} with ratio {}:{}. '
                             'Return of old shares.').format(
                                 security, execute_at.date(),
                                 int(dividend), int(divisor)),
            }
            if shareholder.pk == company_shareholder.pk:
                kwargs1.update(dict(buyer=None, count=self.share_count,
                    value=shareholder.buyer.first().value))
            p = Position.objects.create(**kwargs1)
            logger.info('Split: share returned {}'.format(p))

            part, count2 = math.modf(count * divisor / dividend)
            kwargs2 = {
                'buyer': shareholder,
                'seller': company_shareholder,
                'count': count2,
                'value': value / divisor * dividend,
                'security': security,
                'bought_at': execute_at,
                'is_split': True,
                'comment': _('Share split of {} on {} with ratio {}:{}. '
                             'Provisioning of new shares.').format(
                                 security, execute_at.date(),
                                 int(dividend), int(divisor)),
            }
            if shareholder.pk == company_shareholder.pk:
                part, count2 = math.modf(
                    self.share_count /
                    dividend * float(divisor)
                )
                kwargs2.update({
                    'count': count2,
                    'seller': None,
                })

            p = Position.objects.create(**kwargs2)
            if part != 0.0:
                partials.update({shareholder.pk: round(part, 6)})
            logger.info('Split: share issued {}'.format(p))

        # update share count
        self.share_count = int(
            self.share_count / dividend * float(divisor)
        )

        # record partial shares to operator
        self._send_partial_share_rights_email(partials)

        self.save()


class UserProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)

    company_name = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "%s, %s %s" % (self.city, self.province,
                              str(self.country))

    class Meta:
        verbose_name_plural = "UserProfile"


class Shareholder(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company', verbose_name="Shareholders Company")
    number = models.CharField(max_length=255)

    def __str__(self):
        return u'{}'.format(self.id)

    def share_percent(self, date=None):
        """ returns percentage of shares owned compared to corps
        total shares
        FIXME returns wrong values if the company still holds shares
        after capital increase, which are not distributed to shareholders
        company would then have a percentage of itself, although this is
        not relevant for voting rights, etc.
        """
        total = self.company.share_count
        count = sum(self.buyer.all().values_list('count', flat=True)) - \
            sum(self.seller.all().values_list('count', flat=True))
        if total:
            return "{:.2f}".format(count / float(total) * 100)
        return False

    def share_count(self, date=None, security=None):
        """ total count of shares for shareholder  """
        date = date or datetime.datetime.now()
        qs_bought = self.buyer.all()
        qs_sold = self.seller.all()

        if date:
            qs_bought = self.buyer.filter(bought_at__lte=date)
            qs_sold = self.seller.filter(bought_at__lte=date)

        if security:
            qs_bought = qs_bought.filter(security=security)
            qs_sold = qs_sold.filter(security=security)

        count_bought = sum(qs_bought.values_list('count', flat=True))
        count_sold = sum(qs_sold.values_list('count', flat=True))

        return count_bought - count_sold

    def share_value(self, date=None):
        """ calculate the total values of all shares for this shareholder """
        share_count = self.share_count(date=date)
        if share_count == 0:
            return 0

        # last payed price
        position = Position.objects.filter(buyer__company=self.company).latest(
            'bought_at')
        return share_count * position.value

    def last_traded_share_price(self, date=None, security=None):
        qs = Position.objects.filter(buyer__company=self.company)
        if date:
            qs = qs.filter(bought_at__lte=date)
        if security:
            qs = qs.filter(security=security)
        if not qs.exists():
            raise ValueError(
                'No Transactions available to calculate recent share price')

        return qs.latest('bought_at').value

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
    company = models.ForeignKey('Company', verbose_name="Operators Company")
    share_count = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return u"{} {} ({})".format(self.user.first_name, self.user.last_name, self.user.email)

    def __unicode__(self):
        return u"{} {} ({})".format(self.user.first_name, self.user.last_name, self.user.email)

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

    buyer = models.ForeignKey('Shareholder', related_name="buyer", blank=True, null=True)
    seller = models.ForeignKey('Shareholder', blank=True, null=True,
                               related_name="seller")
    security = models.ForeignKey(Security)
    count = models.PositiveIntegerField(_('Share Count transfered or created'))
    bought_at = models.DateField()
    value = models.DecimalField(
        _('Nominal value or payed price for the transaction'),
        max_digits=8, decimal_places=4, blank=True,
        null=True)
    is_split = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"Pos {}->#{}@{}->{}".format(
            self.seller,
            self.count,
            self.value,
            self.buyer
        )


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
        return "/optionsplan/{}/download/img/?t={}".format(
            self.pk, time.time())

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
        UserProfile.objects.create(user=instance)
