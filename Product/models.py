from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name="products")
    name = models.CharField(max_length=255)
    new_price = models.FloatField(null=True, blank=True)
    price = models.FloatField()
    rate = models.FloatField(null=True, blank=True)
    text = models.TextField()
    image1 = models.ImageField(upload_to="images/", null=True, blank=True)
    image2 = models.ImageField(upload_to="images/", null=True, blank=True)
    image3 = models.ImageField(upload_to="images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name



from django.db import models
from django.conf import settings  # CustomUser ni olish uchun
from django.contrib.auth import get_user_model


User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    is_completed = models.BooleanField(default=False)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        if self.product.new_price > 0:
            return self.product.new_price * self.quantity
        else:
            return self.product.price * self.quantity
