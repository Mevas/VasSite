from django.conf.urls import url

from . import views

urlpatterns = [
    url('undercutter/', views.undercutter, name='undercutter'),
    url('program-scraper/', views.program_scraper, name='program_scraper'),
    url('', views.index, name='index')
]
