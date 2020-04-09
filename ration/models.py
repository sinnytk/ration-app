from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils import timezone
class RationAllocation(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )
    cnic = models.CharField(max_length=13, validators=[RegexValidator(regex='^[\d]{13}$', message='CNIC can only be 13 digit number', code='nomatch')], primary_key=True)
    org_name = models.CharField(max_length=150, default='', blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.created:
            self.created = timezone.localtime(timezone.now())
        self.modified = timezone.localtime(timezone.now())
        return super(RationAllocation, self).save(*args, **kwargs)