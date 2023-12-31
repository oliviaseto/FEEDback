from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.core.serializers import serialize
from django.utils import timezone
from .models import User, Restaurant, Review
from .forms import RestaurantForm, ReviewForm, AdminMessageForm
import urllib.request, json 

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

            #profile_url = f'/feedback/user-profile/' if user_type == 'user' else f'/feedback/admin-profile/'
            #return redirect(profile_url)
            return redirect(f'/feedback/restaurant-list/')
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
    restaurants = Restaurant.objects.filter(approved=True)
    # context = {
    #     'restaurants': Restaurant.objects.all(),
    #     'restaurants_json': serializers.serialize('json', restaurants)
    # }
    context = {
        'restaurants': restaurants,
        'restaurants_json': serialize('json', restaurants, use_natural_primary_keys=True)
    }
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
            review.rating = request.POST.get('rating')  
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
    # if not request.user.is_admin:
    #     return HttpResponseRedirect('/feedback/restaurant-list/')  # Redirect non-admins to a different page
    message = ""

    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            street_address = form.cleaned_data['street_address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']

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

            state_for_url = "+" + state + "+" + str(zip_code)

            location_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + street_address_for_url + city_for_url + state_for_url + '&key=AIzaSyCaoOcQLJHlgQQyc98Wfw_dpA6j3H4c70M'
            # has to follow this format: 
            # https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyCaoOcQLJHlgQQyc98Wfw_dpA6j3H4c70M
            print(location_url)
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
            restaurant.user = request.user
            if request.user.is_admin:
                restaurant.approved = True
                restaurant.not_approved = False
                restaurant.is_rejected = False
            else:
                restaurant.approved = False
                restaurant.not_approved = True
                restaurant.is_rejected = False
                message = "Your request for a new restaurant to be added has been submitted and is pending admin approval."
            restaurant.save()
            form = RestaurantForm()

            if request.user.is_admin:
                return HttpResponseRedirect('/feedback/restaurant-list/')  # Redirect to the restaurant list
            else:
                return render(request, 'feedback/submit_restaurant.html', {'form': form, 'user': request.user, "message": message})

    else:
        form = RestaurantForm()

    return render(request, 'feedback/submit_restaurant.html', {'form': form, 'user': request.user, "message": message})

def approve_reviews(request):
    if not request.user.is_admin:
        return redirect('feedback:restaurant_list') 

    pending_reviews = Review.objects.filter(not_approved=True)

    if request.method == 'POST':
        review_id = request.POST.get('review_id')  
        review = Review.objects.get(pk=review_id)
        review.approved = True
        review.not_approved = False
        review.approved_at = timezone.now()  # Set the approval timestamp
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
    
def approve_or_reject_restaurants(request):
    pending_restaurants = Restaurant.objects.filter(not_approved=True)

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        form = AdminMessageForm(request.POST, instance=restaurant)

        if form.is_valid():
            admin_message = form.cleaned_data['admin_message']
            action = request.POST.get('action')

            if action == 'approve':
                restaurant.approved = True
                restaurant.not_approved = False
                restaurant.is_rejected = False
                restaurant.approved_at = timezone.now()  # Set the approval timestamp
            elif action == 'reject':
                restaurant.approved = False
                restaurant.is_rejected = True
                restaurant.not_approved = False

            restaurant.admin_message = admin_message
            restaurant.save()

            return redirect('feedback:approve_or_reject_restaurants')

    else:
        form = AdminMessageForm()

    context = {
        'form': form,
        'pending_restaurants': pending_restaurants,
    }

    return render(request, 'feedback/approve_or_reject_restaurants.html', context)

class UserSumbittedRestaurantListView(View):
    template_name = 'feedback/user_submitted_restaurant_list.html'

    def get_context_data(self, **kwargs):
        context = {}
        user = self.request.user
        pending_restaurants = Restaurant.objects.filter(user=user, not_approved=True)
        approved_restaurants = Restaurant.objects.filter(user=user, approved=True)
        rejected_restaurants = Restaurant.objects.filter(user=user, is_rejected=True)
        context['pending_restaurants'] = pending_restaurants
        context['approved_restaurants'] = approved_restaurants
        context['rejected_restaurants'] = rejected_restaurants
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
    
# ***************************************************************************************
# *  REFERENCES
# *  Title: django-allauth: Retrieve First/Last Names from FB, Twitter, Google
# *  Author: Shacker
# *  Date: December 3, 2013
# *  URL: https://blog.birdhouse.org/2013/12/03/django-allauth-retrieve-firstlast-names-from-fb-twitter-google/
# * 
# *  Title: User Registration in Django using Google OAuth
# *  Author: Geoffrey Mungai
# *  Date: December 18, 2020
# *  URL: https://www.section.io/engineering-education/django-google-oauth/
# ***************************************************************************************  