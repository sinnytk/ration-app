from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="home"),
    path('add',views.add_record, name="add-record"),
    path('search',views.search_record, name="search-record")

]
