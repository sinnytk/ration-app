from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="home"),
    path('add',views.AddRecord.as_view(), name="add-record"),
    path('search',views.SearchRecord.as_view(), name="search-record"),
    path('add/successful',views.AddRecord.as_view(), name="record_added"),
    

]
