from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg, Count
from django.utils import timezone

class User(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField()

    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lng = models.DecimalField(max_digits=10, decimal_places=7)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)  
    not_approved = models.BooleanField(default=True) 
    is_rejected = models.BooleanField(default=False)  
    admin_message = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)

    def average_rating(self):
        reviews = Review.objects.filter(restaurant=self, approved=True).aggregate(average=Avg('rating'))
        avg = reviews["average"] or 0
        return avg

    def count_reviews(self):
        reviews = Review.objects.filter(restaurant=self, approved=True).aggregate(count=Count('id'))
        count = reviews["count"] or 0
        return count

    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    approved = models.BooleanField(default=False)  
    not_approved = models.BooleanField(default=True) 
    is_rejected = models.BooleanField(default=False)  
    rating = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Review for {self.restaurant.name} by {self.user.username}"

# ***************************************************************************************
# *  REFERENCES
# *  Title: How to Implement Multiple User Types with Django
# *  Author: Vitor Freitas
# *  Date: January 18, 2018
# *  URL: https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html#:~:text=For%20that%20case%2C%20you%20can,in%20the%20Django%20Admin%20pages
# *
# *  Title: auth.User.groups: (fields.E304) Reverse accessor for 'User.groups' clashes with reverse accessor for 'UserManage.groups'
# *  Author: aircraft
# *  Date: March 9, 2018
# *  URL: https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html#:~:text=For%20that%20case%2C%20you%20can,in%20the%20Django%20Admin%20pages
# *
# *  Title: How to Show Average of Star Rating in django
# *  Author: santosh Chauhan
# *  Date: July 6, 2021
# *  URL: https://stackoverflow.com/questions/68255990/how-to-show-average-of-star-rating-in-django
# ***************************************************************************************  