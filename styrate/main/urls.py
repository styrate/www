from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import  settings

urlpatterns = [
    path('', views.renderIndex, name='renderIndex'),
    path('account', views.renderAccountPage, name='renderAccountPage'),
    path('review/<str:reviewID>', views.renderReviewPage, name='renerReviewPage'),
    path('newComment', views.newComment, name='newComment'),
    path('logout', views.logOut, name='logOut'),
    path('login', views.renderlogIn, name='renderLogIn'),
    path('register', views.renderRegister, name='renderRegister')
] + static('/css/', document_root = settings.CSS_ROOT)