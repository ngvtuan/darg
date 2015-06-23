from django.db import models
from django.conf import settings

class Country(models.Model):
    """Model for countries"""
    iso_code = models.CharField(max_length = 2, primary_key = True)
    name = models.CharField(max_length = 45, blank = False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name", "iso_code"]


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255, blank = False, null=True)
    postal_code = models.CharField(max_length=255)
    country = models.ForeignKey(Country, blank = False)

    company_name = models.CharField(max_length=255, blank = False, null=True)
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
    # security = models.ForeignKey(Security) # company specific security type

    def __str__(self):
        return u"{} {} ({})".format(self.user.first_name, self.user.last_name, self.number)

    def share_percent(self):
        """ returns percentage of shares owned compared to corps total shares """
        total = self.company.share_count
        count = sum(self.buyer.all().values_list('count', flat=True)) - \
            sum(self.seller.all().values_list('count', flat=True))
        if total:
            return count / float(total) * 100
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

        #last payed price
        position = Position.objects.filter(buyer__company=self.company).latest('bought_at')
        return share_count * position.value

        

class Operator(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company')
    share_count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return u"{} {}".format(self.user.first_name, self.user.last_name)

class Position(models.Model):

    buyer = models.ForeignKey('Shareholder', related_name="buyer")
    seller = models.ForeignKey('Shareholder', blank=True, null=True, related_name="seller")
    count = models.IntegerField()
    bought_at = models.DateField()
    value = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)

class Company(models.Model):

    name = models.CharField(max_length=255)
    share_count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return u"{}".format(self.name)


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
