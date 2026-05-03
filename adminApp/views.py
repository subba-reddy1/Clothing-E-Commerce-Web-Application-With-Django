from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from usersApp.models import Product, Order, OrderItem, OrderStatusHistory
from .forms import ProductForm

# --- MAIN DASHBOARD ---
@staff_member_required(login_url='login')
def dashboard(request):
    # 1. Calculate Stats for the "Cards" at the top
    # (You can eventually replace the static revenue with: sum(order.total_amount for order in Order.objects.all()))
    total_revenue = 840000 
    active_orders = Order.objects.count()
    total_products = Product.objects.count()

    # 2. Get the Product List for the "Table" at the bottom
    products = Product.objects.all().order_by('-id') 

    context = {
        'revenue': total_revenue,
        'orders_count': active_orders,
        'products_count': total_products,
        'products': products  # We pass this so we can list them in the dashboard table
    }
    return render(request, 'adminApp/dashboard.html', context)

# --- PRODUCT MANAGEMENT ---
@staff_member_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("✅ Product Saved Successfully!")
            return redirect('manager_dashboard')
        else:
            # --- ADD THIS DEBUGGING BLOCK ---
            print("❌ FORM INVALID! Here are the errors:")
            print(form.errors) 
            # --------------------------------
    else:
        form = ProductForm()
    
    return render(request, 'adminApp/add_product.html', {'form': form})

@staff_member_required(login_url='login')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    # CHANGE THIS LINE TOO:
    return redirect('manager_dashboard')

# --- ORDERS & USERS ---
@staff_member_required(login_url='login')
def view_orders(request):
    orders = Order.objects.all().select_related('user').order_by('-ordered_at')
    return render(request, 'adminApp/view_orders.html', {'orders': orders})


@staff_member_required(login_url='login')
def order_detail(request, order_id):
    """Secure admin-only order details page."""
    order = get_object_or_404(
        Order.objects.select_related('user').prefetch_related('items__product'),
        pk=order_id
    )
    history = order.status_history.all().order_by('-changed_at')[:20]
    allowed_next = order.get_allowed_next_statuses()
    context = {
        'order': order,
        'status_history': history,
        'allowed_next_statuses': allowed_next,
    }
    return render(request, 'adminApp/order_detail.html', context)


@staff_member_required(login_url='login')
@require_http_methods(["POST"])
def order_update_status(request, order_id):
    """Update order status with backend validation; admin only."""
    order = get_object_or_404(Order, pk=order_id)
    new_status = request.POST.get('new_status', '').strip()
    if not new_status:
        messages.error(request, 'No status selected.')
        return redirect('admin_order_detail', order_id=order_id)
    if not order.can_transition_to(new_status):
        messages.error(
            request,
            f'Invalid transition: cannot change from {order.status} to {new_status}.'
        )
        return redirect('admin_order_detail', order_id=order_id)
    from_status = order.status
    order.status = new_status
    order.save(update_fields=['status', 'updated_at'])
    OrderStatusHistory.objects.create(
        order=order,
        from_status=from_status,
        to_status=new_status,
        changed_by=request.user,
    )
    messages.success(request, f'Order status updated to {new_status}.')
    return redirect('admin_order_detail', order_id=order_id)

@staff_member_required(login_url='login')
def view_users(request):
    # Placeholder for user management
    return render(request, 'adminApp/view_users.html')

@staff_member_required(login_url='login')
def sales_report(request):
    # Placeholder for sales reports
    return render(request, 'adminApp/sales_report.html')