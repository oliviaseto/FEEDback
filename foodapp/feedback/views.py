from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from .models import User, Restaurant, Review
from .forms import RestaurantForm, ReviewForm
import urllib.request, json 
from django.core import serializers
from django.core.serializers import serialize
from django.http import JsonResponse

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
            pending_reviews = Review.objects.filter(not_approved=True)
            context['pending_reviews'] = pending_reviews

        return render(request, self.template_name, context)

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    # context = {
    #     'restaurants': Restaurant.objects.all(),
    #     'restaurants_json': serializers.serialize('json', restaurants)
    # }
    context = {
        'restaurants': Restaurant.objects.all(),
        'restaurants_json': serialize('json', restaurants, use_natural_primary_keys=True)
    }
    print(context['restaurants_json'])
    return render(request, 'feedback/restaurant_list.html', context)

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant, approved=True)
    message = ""

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.restaurant = restaurant
            review.approved = False  # By default, not approved
            review.not_approved = True  # By default, pending approval
            review.save()
            message = "Your review has been submitted and is pending admin approval."
            form = ReviewForm()
        else:
            message = "Review submission failed. Please correct the errors."
    else:
        form = ReviewForm()

    # map url construction 
    # has to follow this format: 
    # "https://www.google.com/maps/embed/v1/place?key=API_KEY&q=Space+Needle,Seattle+WA"

    name_list = restaurant.name.split(" ")
    name_for_url = ''
    for part in range(len(name_list)):
        if part != len(name_list):
            name_for_url += name_list[part] + '+'
        else:
            name_for_url += name_list[part] + ','

    city_list = restaurant.city.split(" ")
    city_for_url = ''
    for part in range(len(city_list)):
        if part == 0:
            name_for_url += city_list[part] 
        else:
            name_for_url += name_list[part] + '+'

    state = restaurant.state

    map_url = 'https://www.google.com/maps/embed/v1/place?key=AIzaSyCaoOcQLJHlgQQyc98Wfw_dpA6j3H4c70M&q=' + name_for_url + city_for_url + '+' + state
    
    context = {
        'restaurant': restaurant,
        'reviews': reviews,
        'user': request.user,
        'review_form': form,  
        'message': message,
        'map_url': map_url
    }

    return render(request, 'feedback/restaurant_detail.html', context)

def submit_restaurant(request):
    if not request.user.is_admin:
        return HttpResponseRedirect('/feedback/restaurant-list/')  # Redirect non-admins to a different page

    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            street_address = form.cleaned_data['street_address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']

            street_address_for_url = ''
            street_address_list = street_address.split(" ")
            for part in range(len(street_address_list)-1):
                if part != len(street_address_list)-1:
                    street_address_for_url += street_address_list[part] + "+"
                else:
                    street_address_for_url += street_address_list[part] + ","

            city_for_url = ''
            city_list = city.split(" ")
            for part in range(len(city_list)-1):
                if part != len(city_list)-1:
                    city_for_url += "+" + city_list[part]
                else:
                    city_for_url += "+" + city_list[part] + ","

            state_for_url = "+" + state

            location_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + street_address_for_url + city_for_url + state_for_url + '&key=AIzaSyCaoOcQLJHlgQQyc98Wfw_dpA6j3H4c70M'
            # has to follow this format: 
            # https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyCaoOcQLJHlgQQyc98Wfw_dpA6j3H4c70M

            lat = 0.0
            lng = 0.0
            with urllib.request.urlopen(location_url) as url:
                data = json.load(url)
                lat_lng_data = data["results"][0]["geometry"]["location"]
                lat = lat_lng_data['lat']
                lng = lat_lng_data['lng']

            restaurant = form.save(commit=False)
            restaurant.name = name
            restaurant.street_address = street_address
            restaurant.city = city
            restaurant.state = state
            restaurant.lat = lat
            restaurant.lng = lng
            restaurant.save()

            return HttpResponseRedirect('/feedback/restaurant-list/')  # Redirect to the restaurant list

    else:
        form = RestaurantForm()

    return render(request, 'feedback/submit_restaurant.html', {'form': form})

def approve_reviews(request):
    if not request.user.is_admin:
        return redirect('feedback:restaurant_list') 

    pending_reviews = Review.objects.filter(not_approved=True)

    if request.method == 'POST':
        review_id = request.POST.get('review_id')  
        review = Review.objects.get(pk=review_id)
        review.approved = True
        review.not_approved = False
        review.save()

        # Redirect to the same page 
        return redirect('feedback:approve_reviews')

    context = {
        'pending_reviews': pending_reviews,
    }

    return render(request, 'feedback/approve_reviews.html', context)

def reject_review(request):
    if not request.user.is_admin:
        return redirect('feedback:restaurant_list')  

    if request.method == 'POST':
        review_id = request.POST.get('review_id')  
        review = Review.objects.get(pk=review_id)
        review.is_rejected = True
        review.not_approved = False
        review.save()

        # Redirect to the same page 
        return redirect('feedback:approve_reviews')  

    return redirect('feedback:approve_reviews') 

class ReviewListView(View):
    template_name = 'feedback/review_list.html'

    def get_context_data(self, **kwargs):
        context = {}
        user = self.request.user
        pending_reviews = Review.objects.filter(user=user, not_approved=True)
        approved_reviews = Review.objects.filter(user=user, approved=True)
        rejected_reviews = Review.objects.filter(user=user, is_rejected=True)
        context['pending_reviews'] = pending_reviews
        context['approved_reviews'] = approved_reviews
        context['rejected_reviews'] = rejected_reviews
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)