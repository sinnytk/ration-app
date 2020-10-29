from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta

class Person(models.Model):
    cnic = models.CharField(max_length=13, validators=[RegexValidator(regex='^[\d]{13}$', message='CNIC can only be 13 digit number', code='nomatch')], primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, default='',blank=True)
    address = models.CharField(max_length=500, default='',blank=True)
    family_count = models.PositiveSmallIntegerField(default=1,blank=True)
class RationAllocation(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        blank=True, 
        null=True
    )
    org_name = models.CharField(max_length=150, default='', blank=True)
    created = models.DateTimeField(editable=False)
    allocation_expiry = models.DateTimeField(default=timezone.localtime(timezone.now()+timedelta(days=1)))
    modified = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.created:
            self.created = timezone.localtime(timezone.now())
        self.modified = timezone.localtime(timezone.now())
        self.org_name = self.org_name.upper()
        if (self.allocation_expiry - self.created).days < 0:
            self.allocation_expiry = timezone.localtime(timezone.now()+timedelta(days=1))
        return super(RationAllocation, self).save(*args, **kwargs)