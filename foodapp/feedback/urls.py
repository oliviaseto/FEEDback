from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views

app_name = 'feedback'
urlpatterns = [
    # path('register/user/', views.register_user, name='register_user'),
    # path('register/admin/', views.register_admin, name='register_admin'),
    path('user-profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('admin-profile/', views.AdminProfileView.as_view(), name='admin_profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('complete/google-oauth2/<str:user_type>/', views.CompleteGoogleOAuth2View.as_view(), name='complete_google_oauth2'),
]