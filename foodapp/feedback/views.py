from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import User, Restaurant, Review
from .forms import RestaurantForm

class CompleteGoogleOAuth2View(View):
    def get(self, request, user_type):
        if request.user.is_authenticated and request.user.socialaccount_set.filter(provider='google').exists():
            google_account = request.user.socialaccount_set.get(provider='google')

            if user_type == 'admin':
                user, created = User.objects.get_or_create(email=google_account.extra_data['email'])
                user.username = google_account.extra_data['email']
                user.name = google_account.extra_data['name']
                user.is_admin = True
            else:
                user, created = User.objects.get_or_create(email=google_account.extra_data['email'])
                user.username = google_account.extra_data['email']
                user.name = google_account.extra_data['name']
                user.is_user = True
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.save()

            login(request, user)

            profile_url = f'/feedback/user-profile/' if user_type == 'user' else f'/feedback/admin-profile/'
            return redirect(profile_url)
        return

class UserProfileView(LoginRequiredMixin, View):
    template_name = 'feedback/user_profile.html'

    def get_context_data(self, **kwargs):
        context = {'user': self.request.user}
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

class AdminProfileView(LoginRequiredMixin, View):
    template_name = 'feedback/admin_profile.html'

    def get_context_data(self, **kwargs):
        context = {'user': self.request.user}
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})

@login_required
def submit_review(request, restaurant_id):
    if request.method == 'POST':
        user = request.user
        content = request.POST.get('content')
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        Review.objects.create(restaurant=restaurant, user=user, content=content)

    return redirect('restaurant_detail', restaurant_id=restaurant_id)

@login_required
def restaurant_detail(request, restaurant_id):
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant, approved=True)
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant, 'reviews': reviews})

@login_required
def submit_restaurant(request):
    if not request.user.is_staff:
        return redirect('restaurant_list')  # Redirect non-admins to a different page

    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')

    else:
        form = RestaurantForm()

    return render(request, 'feedback/submit_restaurant.html', {'form': form})

@login_required
def admin_review_management(request):
    if not request.user.is_staff:
        return redirect('restaurant_list')  # Redirect non-admins to a different page

    pending_reviews = Review.objects.filter(approved=False)
    return render(request, 'admin_review_management.html', {'pending_reviews': pending_reviews})

@login_required
def approve_review(request, review_id):
    if not request.user.is_staff:
        return redirect('restaurant_list')  # Redirect non-admins to a different page

    review = Review.objects.get(pk=review_id)
    review.approved = True
    review.save()
    return redirect('admin_review_management')

# @login_required
# def register_user(request):
#     return redirect('user_profile')

# @login_required
# def register_admin(request):
#     return redirect('admin_profile')
