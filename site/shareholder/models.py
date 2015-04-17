from django.db import models
from django.conf import settings


class Shareholder(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company')
    number = models.CharField(max_length=255)

    def __str__(self):
        return "{} {} ({})".format(self.user.first_name, self.user.last_name, self.number)

class Operator(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey('Company')

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

class Position(models.Model):

    shareholder = models.ForeignKey('Shareholder')
    count = models.IntegerField()
    bought_at = models.DateField()
    sold_at = models.DateField()

class Company(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
