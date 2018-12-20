from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import AbstractUser, Group
from datetime import date
import re

# TODO: add group

""" Manager Classes """
class CupInAdminManager(models.Manager):
    def get_queryset(self):
        return super(CupInAdminManager, self).get_queryset().filter(owner_type='a') 

class Cup(models.Model):
    # TODO: RFID 
    objects = models.Manager()
    in_admin = CupInAdminManager()

    LOAN_STATUS = (
        ('o', 'On loan'),
        ('c', 'Cleaning'),
        ('a', 'Available'),
        ('n', 'Not in circulation')
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        default='r',
        help_text='Cup availability',
    )
    CARRIER_TYPES = (
        ('b', 'Business'),
        ('u', 'User'),
        ('a', 'Administration'),
        ('m', 'Machine')
    )
    carrier_type = models.CharField(max_length=1, choices = CARRIER_TYPES, default='a')
    carrier = models.ForeignKey('CupUser', on_delete=models.SET_NULL, blank=True, null=True)

    # TODO: add to the action when user checks out a cup
    checked_out_date = models.DateField(null=True, blank=True)

    @property
    def duration(self):
        if self.checked_out_date :
            return (date.today() - self.checked_out_date).days
        return None

    def __str__(self):
        return str(self.pk)

class CupUser(AbstractUser):
    phone_number = models.CharField(blank=True, null=True, max_length=10, help_text='e.g. 0912345678')
    address = models.CharField(blank=True, null=True, max_length=300, help_text='貴公司地址')
    title = models.CharField(blank=True, null=True, max_length=300, help_text='貴公司名稱')

    # staff(built-in), customer, business
    is_customer = models.BooleanField(default=False, verbose_name='customer status')
    is_business = models.BooleanField(default=False, verbose_name='business status')

    @property
    def name(self):
        if self.first_name and self.last_name:
            english = r'(^[A-Za-z]+$)'
            if re.match(english, self.first_name+self.last_name):
                return ("%s %s" % (self.first_name, self.last_name))
            else:
                return self.last_name+self.first_name
        elif self.title:
            return self.title
        else:
            return self.username

    def __str__(self):
        return self.name


class Record(models.Model):
    cup = models.ForeignKey('Cup', on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    prev_carrier = models.ForeignKey('CupUser', related_name='prev_carrier', on_delete=models.SET_NULL, blank=True, null=True) 
    current_carrier = models.ForeignKey('CupUser', related_name='current_carrier', on_delete=models.SET_NULL, blank=True, null=True) 

    def __str__(self):
        return str("from %s to %s" % prev_carrier.name, current_carrier.name)




