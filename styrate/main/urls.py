from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import  settings

urlpatterns = [
    path('test/test', views.testPoint, name='testPoint'),
    path('', views.renderIndex, name='renderIndex')
] + static('/css/', document_root = settings.CSS_ROOT)