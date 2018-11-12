from django.conf.urls import url
from . import views

urlpatterns = [
    url('undercutter/', views.undercutter, name='undercutter'),
    url('', views.index, name='index')
]
