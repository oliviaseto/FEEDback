from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views

app_name = 'feedback'
urlpatterns = [
    path('user-profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('admin-profile/', views.AdminProfileView.as_view(), name='admin_profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('complete/google-oauth2/<str:user_type>/', views.CompleteGoogleOAuth2View.as_view(), name='complete_google_oauth2'),
    path('restaurant-list/', views.restaurant_list, name='restaurant_list'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('submit-restaurant/', views.submit_restaurant, name='submit_restaurant'),
    path('approve-reviews/', views.approve_reviews, name='approve_reviews'), 
    path('review-list/', views.ReviewListView.as_view(), name='review_list'),
    path('reject-review/', views.reject_review, name='reject_review'),
]