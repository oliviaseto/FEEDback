from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
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

        if request.user.is_admin:
            print(request.user.is_admin)  # Add this line for debugging
            pending_reviews = Review.objects.filter(not_approved=True)
            context['pending_reviews'] = pending_reviews

        return render(request, self.template_name, context)

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'feedback/restaurant_list.html', {'restaurants': restaurants})

def submit_review(request, restaurant_id):
    if request.method == 'POST':
        user = request.user
        content = request.POST.get('content')
        approved = False  # By default, a user-submitted review is not approved
        not_approved = True  # By default, a user-submitted review is pending approval
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        Review.objects.create(restaurant=restaurant, user=user, content=content, approved=approved, not_approved=not_approved)

    return redirect('restaurant_detail', restaurant_id=restaurant_id)

def submit_restaurant(request):
    if not request.user.is_admin:
        return HttpResponseRedirect('/feedback/restaurant-list/')  # Redirect non-admins to a different page

    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/feedback/restaurant-list/')  # Redirect to the restaurant list

    else:
        form = RestaurantForm()

    return render(request, 'feedback/submit_restaurant.html', {'form': form})

def approve_review(request, review_id):
    if not request.user.is_admin:
        return redirect('feedback:restaurant_list')  # Redirect non-admins to a different page

    review = Review.objects.get(pk=review_id)
    review.approved = True
    review.not_approved = False  # Mark the review as approved
    review.save()
    return redirect('admin_profile')

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)  # Use get_object_or_404
    reviews = Review.objects.filter(restaurant=restaurant, approved=True)

    context = {
        'restaurant': restaurant,
        'reviews': reviews,
        'user': request.user,
    }

    return render(request, 'feedback/restaurant_detail.html', context)
