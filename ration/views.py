from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView
from .models import RationAllocation
from .forms import RationAllocationCreateForm, RationAllocationRetrieveForm
from django.urls import reverse_lazy
from django.db.models import Count

@login_required
def index(request):
    allocations_from_db = RationAllocation.objects.all()
    allocations_count = len(allocations_from_db)
    allocations = allocations_from_db.values('org_name','user__email').annotate(total=Count('org_name')).order_by('-total')[:5]
    return render(request, "ration/homepage.html", context={'page_name':"Dashboard","allocations":allocations,"allocations_count":allocations_count})

class AddRecord(LoginRequiredMixin, CreateView):
    model = RationAllocation
    template_name="ration/add_record.html"
    form_class = RationAllocationCreateForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.save()
        return render(self.request, 'ration/record_added.html', context={'page_name':"Add Record",'CNIC':form.cleaned_data['cnic']})
    
    def get_context_data(self, **kwargs):
        ctx = super(AddRecord, self).get_context_data(**kwargs)
        ctx['page_name'] = "Add Record"
        return ctx
        
class SearchRecord(LoginRequiredMixin, FormView):
    model = RationAllocation
    template_name="ration/search_record.html"
    form_class = RationAllocationRetrieveForm
    def form_valid(self, form):
        obj = form.get_allocation()
        return render(self.request, 'ration/searched_record.html', context={'page_name':"Search Record","allocation":obj,'CNIC':form.cleaned_data['cnic']})
    
    def get_context_data(self, **kwargs):
        ctx = super(SearchRecord, self).get_context_data(**kwargs)
        ctx['page_name'] = "Search Record"
        return ctx