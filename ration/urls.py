from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="home"),
    path('add',views.GenerateForm.as_view(), name="generate-form"),
    path('add/new',views.add_person_and_allocation, name="new-form"),
    path('add/allocation',views.add_allocation, name="allocation-form"),
    path('search',views.SearchRecord.as_view(), name="search-record"),
    

]
