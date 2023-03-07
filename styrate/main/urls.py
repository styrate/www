from django.urls import path
from . import views

urlpatterns = [
    path('test/test', views.testPoint, name='testPoint'),
    path('', views.renderIndex, name='renderIndex')
]