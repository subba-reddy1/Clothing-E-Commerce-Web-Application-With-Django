from django.contrib import admin
from .models import Product, Category, Size, Color, Order, OrderItem, OrderStatusHistory, Cart

# 1. Register Attribute Models
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Color)

# 2. Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('sizes', 'colors') # Makes selecting many sizes/colors easier

# 3. Order Admin (Advanced)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'size', 'color')

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('from_status', 'to_status', 'changed_at', 'changed_by')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'user', 'total_amount', 'status', 'payment_status', 'ordered_at')
    list_filter = ('status', 'payment_status', 'ordered_at')
    search_fields = ('full_name', 'id', 'phone', 'user__email')
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    
# 4. Cart Admin (Optional - good for debugging)
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'created_at')