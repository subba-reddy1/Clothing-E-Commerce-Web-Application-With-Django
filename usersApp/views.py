from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
import random
import threading 
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Size, Color

# --- 1. EMAIL SYSTEM (Background Sending) ---
class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.message,
            settings.EMAIL_HOST_USER,
            self.recipient_list,
            fail_silently=False,
        )

def send_custom_email(subject, message, to_email):
    EmailThread(subject, message, [to_email]).start()

# --- 2. BASIC PAGES ---
def home(request): return render(request, 'home.html')
def collections(request): return render(request, 'collections.html')
def contact(request): return render(request, 'contact.html')
def about(request): return render(request, 'about.html')

# --- 3. AUTHENTICATION & OTP ---

def unified_login(request):
    """Handles both Admin (Password) and User (OTP) Login"""
    if request.method == 'POST':
        login_type = request.POST.get('login_type')

        # --- ADMIN LOGIN ---
        if login_type == 'admin':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('/manager/dashboard/')
            else:
                return render(request, 'userApp/login.html', {'error': 'Invalid Admin Credentials'})

        # --- USER LOGIN (OTP) ---
        elif login_type == 'user':
            email = request.POST.get('email')
            try:
                # Check if user exists
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'userApp/login.html', {'error': 'User not found. Please Register.'})
            
            # Generate 4-Digit OTP
            otp = str(random.randint(1000, 9999))
            request.session['otp'] = otp
            request.session['otp_email'] = email
            
            
            # Send OTP Email
            subject = "Your StyleHaven Login OTP"
            message = f"Hello {user.username},\n\nYour login code is: {otp}\n\nDo not share this with anyone.\n\n- StyleHaven Team"
            send_custom_email(subject, message, email)
            
            return render(request, 'userApp/verify_otp.html', {'email': email})

    return render(request, 'userApp/login.html')

def verify_otp(request):
    """Checks if the entered OTP matches the session OTP"""
    if request.method == 'POST':
        entered_otp = request.POST.get('otp1') + request.POST.get('otp2') + request.POST.get('otp3') + request.POST.get('otp4')
        if entered_otp == request.session.get('otp'):
            user = User.objects.get(email=request.session.get('otp_email'))
            login(request, user)
            del request.session['otp']  # Clear OTP after use
            return redirect('home')
        else:
            return render(request, 'userApp/verify_otp.html', {'error': 'Invalid OTP', 'email': request.session.get('otp_email')})
    return render(request, 'userApp/verify_otp.html')

def register_view(request):
    """Registers a user and sends a Welcome Email"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Save Email manually
            user.email = request.POST.get('email')
            user.save()

            # Send Welcome Email
            subject = "Welcome to StyleHaven!"
            message = f"Hi {user.username},\n\nThank you for joining StyleHaven!\nWe are excited to have you with us.\n\nHappy Shopping!"
            send_custom_email(subject, message, user.email)

            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'userApp/register.html', {'form': form})

def signout_view(request):
    logout(request)
    return redirect('home')

# --- 4. SHOPPING & ORDERS ---

def products(request):
    """
    List products with dynamic filters:
    - section: men / women / kids / accessories
    - category: specific category inside section (T-shirts, Shirts, etc., by id)
    - q: search text
    - max_price: upper price limit
    """
    products = Product.objects.all()

    section = request.GET.get('section')   # men / women / kids / accessories
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    max_price = request.GET.get('max_price')

    # Filter by section
    if section:
        products = products.filter(category__section=section)
        available_categories = Category.objects.filter(section=section)
    else:
        available_categories = Category.objects.all()

    # Filter by specific category within the section
    if category_id:
        products = products.filter(category_id=category_id)

    # Text search
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Max price filter
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Sort
    sort = request.GET.get('sort', 'newest')
    if sort == 'low_high':
        products = products.order_by('price')
    elif sort == 'high_low':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    # Query string without sort (for building sort dropdown URLs)
    get_copy = request.GET.copy()
    if 'sort' in get_copy:
        get_copy.pop('sort')
    query_no_sort = get_copy.urlencode()

    context = {
        'products': products,
        'categories': available_categories,
        'current_section': section,
        'current_category_id': int(category_id) if category_id else None,
        'current_max_price': max_price,
        'current_sort': sort,
        'query_no_sort': query_no_sort,
    }

    return render(request, 'userApp/products.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'userApp/product_detail.html', {'product': product})

def _get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key: request.session.create()
        cart, _ = Cart.objects.get_or_create(session_id=request.session.session_key)
    return cart

@login_required(login_url='login')
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = _get_cart(request)
    size = None
    color = None
    if request.method == 'POST':
        size_id = request.POST.get('size')
        color_id = request.POST.get('color')
        if size_id: size = Size.objects.get(id=size_id)
        if color_id: color = Color.objects.get(id=color_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size, color=color)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart')

def view_cart(request):
    cart = _get_cart(request)
    items = cart.items.all()
    total = sum(item.total_price for item in items)
    return render(request, 'userApp/cart.html', {'items': items, 'total': total})

def update_cart(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id)
    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        item.quantity -= 1
        if item.quantity <= 0: item.delete()
        else: item.save()
    elif action == 'remove': item.delete()
    return redirect('cart')

@login_required(login_url='login')
def place_order(request):
    """Places an order and sends a Confirmation Email"""
    cart = _get_cart(request)
    items = cart.items.all()
    if not items.exists(): return redirect('products')
    total = sum(item.total_price for item in items)
    
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('name'),
            phone=request.POST.get('mobile'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            subtotal=total,
            discount=0,
            total_amount=total,
        )
        
        # Build Order Email Content
        email_body = f"Hi {request.user.username},\n\nYour order #{order.id} has been confirmed!\n\nHere is what you ordered:\n"
        
        for item in items:
            unit_price = item.product.discount_price or item.product.price
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=unit_price,
                size=getattr(item.size, 'name', '') or '',
                color=getattr(item.color, 'name', '') or '',
            )
            email_body += f"- {item.product.name} (Qty: {item.quantity}) - Rs. {item.total_price}\n"
        
        email_body += f"\nTotal Amount: Rs. {total}\n\nWe will notify you when it ships!\n\nThanks,\nStyleHaven Team"
        
        # Send Order Email
        send_custom_email(f"Order Confirmed: #{order.id}", email_body, request.user.email)

        cart.items.all().delete()
        return redirect('profile')

    return render(request, 'userApp/place_order.html', {'total': total})

@login_required(login_url='login')
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'userApp/profile.html', {'orders': orders})
