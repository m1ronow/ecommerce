from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-id']


class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    company = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=25)
    country = models.CharField(max_length=150)
    post_code = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    full_address = models.CharField(max_length=500)

    class Meta:
        ordering = ['last_name']


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.TextField(blank=True)
    current_address = models.OneToOneField(UserAddress, null=True, on_delete=models.SET_NULL, blank=True)

    class Meta:
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=255)
    icon_name = models.CharField(max_length=255)
    sort_index = models.IntegerField()
    description = models.TextField()

    class Meta:
        ordering = ['sort_index']


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=0, default=1)

    class Meta:
        ordering = ['-quantity']
        unique_together = ('cart', 'product')


class FavoritesItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        unique_together = ('user', 'product')


class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['id']


class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    shipping_method = models.ForeignKey(ShippingMethod, null=True, on_delete=models.SET_NULL)

    # calculated property - total amount to pay for an order
    @property
    def total_price(self):
        # calculate the total price based on OrderItems
        order_items = self.orderitem_set.all()
        subtotal = sum(item.product.price * item.quantity for item in order_items)

        # add the price of the ShippingMethod if it exists
        shipping_price = self.shipping_method.price if self.shipping_method else 0

        # calculate the total price including the shipping price
        total = subtotal + shipping_price

        return total

    class Meta:
        ordering = ['created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        ordering = ['-quantity']


class PaymentMethod(models.Model):
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='payment_logo')

    class Meta:
        ordering = ['id']


class Payment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
    payment_id = models.CharField(max_length=150, blank=True, null=True)
    payment_code = models.CharField(max_length=150, blank=True, null=True)
    hosted_url = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']


class Promo(models.Model):
    discount_code = models.CharField(max_length=50)
    discount_multiplier = models.FloatField()

    class Meta:
        ordering = ['id']
