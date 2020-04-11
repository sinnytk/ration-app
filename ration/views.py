from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView
from .models import RationAllocation
from .forms import RationAllocationCreateForm, RationAllocationRetrieveForm, PersonCreateForm
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone

@login_required
def index(request):
    allocations_from_db = RationAllocation.objects.all()
    allocations_count = len(allocations_from_db)
    allocations = allocations_from_db.values('org_name','user__email').annotate(total=Count('org_name')).order_by('-total')[:5]
    return render(request, "ration/homepage.html", context={'page_name':"Dashboard","allocations":allocations,"allocations_count":allocations_count})


class GenerateForm(LoginRequiredMixin, FormView):    
    
    template_name="ration/add_record.html"
    form_class = RationAllocationRetrieveForm

    def form_valid(self, form):
        person = form.get_person()
        if person:
            last_allocation = RationAllocation.objects.filter(person=person).order_by('-created').last()
            if last_allocation:
                if (last_allocation.allocation_expiry - timezone.localtime(timezone.now())).days >= 0:
                    return render(self.request, 'ration/record_exists.html', context={'page_name':'Add Record','last_allocation':last_allocation})
            else:
                ration_form = RationAllocationCreateForm(initial={'person':person})
                return render(self.request, 'ration/add_record_allocation.html', context={'page_name':"Add Record",'ration_form': ration_form})
        else:
            ration_form = RationAllocationCreateForm(prefix = "ration_allocation")
            person_form = PersonCreateForm(prefix = "person", initial = {'cnic':form.cleaned_data['cnic']})
            return render(self.request, 'ration/add_record_new.html', context={'page_name':"Add Record",'person_form':person_form,'ration_form': ration_form,'CNIC':form.cleaned_data['cnic']})
    def get_context_data(self, **kwargs):
        ctx = super(GenerateForm, self).get_context_data(**kwargs)
        ctx['page_name'] = "Add Record"
        return ctx

@login_required
def add_person_and_allocation(request):
    person_form = PersonCreateForm(request.POST or None, prefix = "person")
    ration_form = RationAllocationCreateForm(request.POST or None, prefix = "ration_allocation")
    if request.method == 'POST':
        person_form = PersonCreateForm(request.POST, prefix = "person")
        ration_form = RationAllocationCreateForm(request.POST, prefix = "ration_allocation")
        if person_form.is_valid() and ration_form.is_valid():
            person = person_form.save()
            ration_form.person = person
            ration = ration_form.save()
            ration.person = person
            ration.user = request.user
            ration.save()
            return render(request, 'ration/record_added.html',context={'page_name':"Add Record",'CNIC':person.cnic, 'expiry_date':ration.allocation_expiry})
    return render(request, 'ration/add_record_new.html', context={
    'page_name':"Add Record",
    'person_form': person_form,
    'ration_form': ration_form,
    })

@login_required
def add_allocation(request):
    ration_form = RationAllocationCreateForm()
    if request.method == 'POST':
        ration_form = RationAllocationCreateForm(request.POST)
        if ration_form.is_valid():
            ration = ration_form.save(commit=False)
            ration.user = request.user
            ration.save()
            return render(request, 'ration/record_added.html',context={'page_name':"Add Record",'CNIC':ration.person.cnic, 'expiry_date':ration.allocation_expiry})
    return render(request, 'ration/add_record_new.html', context={
    'ration_form': ration_form,
    })
class SearchRecord(LoginRequiredMixin, FormView):
    model = RationAllocation
    template_name="ration/search_record.html"
    form_class = RationAllocationRetrieveForm
    def form_valid(self, form):
        person = form.get_person()
        allocations = RationAllocation.objects.filter(person=person).order_by('-created')
        return render(self.request, 'ration/searched_record.html', context={'page_name':"Search Record",'cnic':form.cleaned_data['cnic'],'allocations':allocations})
    
    def get_context_data(self, **kwargs):
        ctx = super(SearchRecord, self).get_context_data(**kwargs)
        ctx['page_name'] = "Search Record"
        return ctx