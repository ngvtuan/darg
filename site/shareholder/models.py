from django.db import models
from django.conf import settings


class Shareholder(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company')
    number = models.CharField(max_length=255)

    def __str__(self):
        return u"{} {} ({})".format(self.user.first_name, self.user.last_name, self.number)

    def share_percent(self):
        """ returns percentage of shares owned compared to corps total shares """
        if not self.buyer.filter(sold_at__isnull=True).count():
            return '-'
        total = self.company.share_count
        count = sum(self.buyer.filter(sold_at__isnull=True).values_list('count', flat=True))
        if total:
            return count / float(total)
        return False

    def share_count(self):   
        """ total count of shares for shareholder  """
        if not self.buyer.filter(sold_at__isnull=True).count():
            return '-'       
        return sum(self.buyer.filter(sold_at__isnull=True).values_list('count', flat=True))

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
    sold_at = models.DateField(blank=True, null=True)
    value = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)

class Company(models.Model):

    name = models.CharField(max_length=255)
    share_count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return u"{}".format(self.name)
