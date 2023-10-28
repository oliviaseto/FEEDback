from django.db import models
from django.contrib.auth.models import AbstractUser

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
    name = models.CharField(max_length=100, unique=True, default="Rice Hall")
    street_address = models.CharField(max_length=100, default="85 Engineer's Way")
    city = models.CharField(max_length=100, default="Charlottesville")
    state = models.CharField(max_length=100, default="VA")

    lat = models.DecimalField(max_digits=9, decimal_places=6, default=38.0316188)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=78.51084589999999)

    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    approved = models.BooleanField(default=False)  
    not_approved = models.BooleanField(default=True) 
    is_rejected = models.BooleanField(default=False)  

    def __str__(self):
        return f"Review for {self.restaurant.name} by {self.user.username}"
