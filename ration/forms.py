from django import forms
from django.core.validators import RegexValidator
from .models import RationAllocation, Person
from django.utils import timezone
from datetime import timedelta

DAY_CHOICES= [tuple([x,x]) for x in range(1,32)]
class PersonCreateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(PersonCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class RationAllocationCreateForm(forms.ModelForm):
    allocation_expiry = forms.ChoiceField(label='Days till ration will last',choices=[(x,x) for x in range(1,11)])
    class Meta:
        model = RationAllocation
        fields = ['person','org_name','allocation_expiry']
        labels = {
            'org_name':('Organization Name')
        }
        widgets = {
            'person':forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        super(RationAllocationCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    def clean_allocation_expiry(self):
        data = self.cleaned_data['allocation_expiry']
        data = timezone.localtime(timezone.now()+timedelta(days=int(data)))
        return data
class RationAllocationRetrieveForm(forms.Form):
    cnic = forms.CharField(max_length=13, validators=[RegexValidator(regex='^[\d]{13}$', message='CNIC can only be 13 digit number', code='nomatch')])
    def __init__(self, *args, **kwargs):
        super(RationAllocationRetrieveForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    def get_person(self):
        cnic = self.cleaned_data['cnic']
        try:
            obj = Person.objects.get(cnic=cnic)
        except Person.DoesNotExist:
            obj = None
        return obj