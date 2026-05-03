from django.db import models
from django.contrib.auth.models import User

# 1. Attributes for Filtering
class Category(models.Model):
    SECTION_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
        ('accessories', 'Accessories'),
    ]

    # High-level section like Men/Women/Kids/Accessories
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='men')

    # Specific category inside the section like T-Shirts, Shirts, Jeans, etc.
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        # Helpful representation in admin
        return f"{self.get_section_display()} - {self.name}"

class Size(models.Model):
    name = models.CharField(max_length=10) # S, M, L, XL
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=20) # Red, Blue
    code = models.CharField(max_length=10) # #FF0000
    def __str__(self):
        return self.name

# 2. Main Product Table
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    sizes = models.ManyToManyField(Size, blank=True) # Product can have multiple sizes
    colors = models.ManyToManyField(Color, blank=True)
    stock = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 3. Shopping Cart (Database-backed for persistence)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * (self.product.discount_price or self.product.price)

# 4. Order System
class Order(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_CONFIRMED = 'Confirmed'
    STATUS_SHIPPED = 'Shipped'
    STATUS_DELIVERED = 'Delivered'
    STATUS_CANCELLED = 'Cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    PAYMENT_PENDING = 'Pending'
    PAYMENT_PAID = 'Paid'
    PAYMENT_FAILED = 'Failed'
    PAYMENT_REFUNDED = 'Refunded'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_PAID, 'Paid'),
        (PAYMENT_FAILED, 'Failed'),
        (PAYMENT_REFUNDED, 'Refunded'),
    ]

    # Allowed status transitions: from_status -> [to_statuses]
    ALLOWED_TRANSITIONS = {
        STATUS_PENDING: [STATUS_CONFIRMED, STATUS_CANCELLED],
        STATUS_CONFIRMED: [STATUS_SHIPPED, STATUS_CANCELLED],
        STATUS_SHIPPED: [STATUS_DELIVERED],
        STATUS_DELIVERED: [],   # terminal
        STATUS_CANCELLED: [],   # terminal
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    ordered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_allowed_next_statuses(self):
        return Order.ALLOWED_TRANSITIONS.get(self.status, [])

    def can_transition_to(self, new_status):
        return new_status in self.get_allowed_next_statuses()

    def __str__(self):
        return f"Order #{self.id} – {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=20, blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.quantity * self.price


class OrderStatusHistory(models.Model):
    """Audit trail for order status changes."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    from_status = models.CharField(max_length=20)
    to_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)