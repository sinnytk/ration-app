from django import forms
from django.core.validators import RegexValidator
from .models import RationAllocation

class RationAllocationCreateForm(forms.ModelForm):
    class Meta:
        model = RationAllocation
        fields = ['cnic','org_name']
    def __init__(self, *args, **kwargs):
        super(RationAllocationCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RationAllocationRetrieveForm(forms.Form):
    cnic = forms.CharField(max_length=13, validators=[RegexValidator(regex='^[\d]{13}$', message='CNIC can only be 13 digit number', code='nomatch')])
    def __init__(self, *args, **kwargs):
        super(RationAllocationRetrieveForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    def get_allocation(self):
        cnic = self.cleaned_data['cnic']
        try:
            obj = RationAllocation.objects.get(cnic=cnic)
        except RationAllocation.DoesNotExist:
            obj = None
        return obj