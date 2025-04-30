from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class ItemList(models.Model):
    category_name = models.CharField(max_length=50)
    def __str__(self):
        return self.category_name
    

class Profile(models.Model):
    USER_TYPES=(
        ('Customer','Customer'),
        ('Vendors','Vendor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=50, choices=USER_TYPES,default='Customer')
    
    def __str__(self):
        return self.user.username    
class AboutUs(models.Model):
    Description = models.TextField()
    
class feedback(models.Model):
    user_name = models.CharField(max_length=50)
    Rating = models.IntegerField()
    Message = models.TextField(blank=False)
    c_image = models.ImageField(upload_to='Items/',default='/')
    def __str__(self):
        return self.user_name
    
    
class BookTable(models.Model):
    user_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    user_email = models.EmailField()
    total_person = models.IntegerField()
    booking_date = models.DateField(null=False, blank=False)  # Temporarily allow null values


    def __str__(self):
        return self.Name
    
class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username
    
class Register(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    def __str__(self):
        return self.username
    
class Items(models.Model):
    Item_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    Category = models.ForeignKey(ItemList, related_name='items', on_delete=models.CASCADE)  # ✅ Fixed related_name
    Image = models.ImageField(upload_to='Items/')

    def __str__(self):
        return self.Item_name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')  #  Removed null=True
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  # Related name is correct
    product = models.ForeignKey(Items, on_delete=models.CASCADE)  # No need for a string reference
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.Item_name} - Quantity: {self.quantity}"

    def get_total_price(self):
        return self.quantity * self.product.price


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default='')
    mobile_number = models.CharField(max_length=20,default='')
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)
    country = models.CharField(max_length=50)
    
    def __str__(self):  
        return f"{self.street}, {self.city}, {self.state}, {self.country}"
    
class Review(models.Model):
    item = models.ForeignKey(Items, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')    
    