from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(80)], null=True,
                                           blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    ROLE_CHOICES = (
        ('host', 'host'),
        ('guest', 'guest'))
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES,max_length=16,default='guest')
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.username}'


class City(models.Model):
    city_name = models.CharField(max_length=30,unique=True)


    def __str__(self):
        return f'{self.city_name}'


class Rules(models.Model):
    rules_image = models.ImageField(upload_to='rules_images')
    rules_name  = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.rules_name


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('Apartment', 'Apartment'),
        ('House', 'House'),
        ('Studio', 'Studio'),
    )
    title = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    property_type = models.CharField(max_length=50,choices=PROPERTY_TYPE_CHOICES)
    rules = models.ManyToManyField(Rules)
    max_guests = models.PositiveSmallIntegerField()
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.property_type}) - {self.city}, Хозяин: {self.owner.username}'

    def get_avg_rating(self):
        ratings = self.property_reviews.all()
        if ratings.exists():
            return round(sum([i.rating for i in ratings]) / ratings.count(), 1)
        return 0
    def get_count_people(self):
        return self.property_reviews.count()

    def get_price_two_night(self):
        return self.price * 2

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='property_images')
    def __str__(self):
        return f'{self.property}, {self.image}'

class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user}, {self.property}'


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE,related_name='property_reviews')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.property}'


