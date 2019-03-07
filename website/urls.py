from django.conf.urls import url
from . import views

urlpatterns = [
    url('auto-undercutter/', views.auto_undercutter, name='auto_undercutter'),
    url('undercutter/', views.undercutter, name='undercutter'),
    url('program-scraper/', views.program_scraper, name='program_scraper'),
    url('', views.index, name='index')
]
