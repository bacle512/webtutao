from django.shortcuts import render
from django.shortcuts import *
from django.http import *
from .models import *
import json
from django.contrib.auth.forms import *
from django.contrib.auth import *
from django.contrib import messages

def home(request):
    if request.user.is_authenticated: #kiểm tra xem user đã đăng nhập chưa
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context = {'items':items, 'cartItems':cartItems, 'user_not_login': user_not_login, 'user_login': user_login, 'categories': categories}
    return render(request, 'app/home.html', context)

def product(request):
    if request.user.is_authenticated: #kiểm tra xem user đã đăng nhập chưa
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    products = Product.objects.all()
    context = {'categories': categories, 'products' : products, 'cartItems' : cartItems, 'user_not_login': user_not_login, 'user_login': user_login, 'items':items, 'active_category':active_category }
    return render(request, 'app/product.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, create = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, create = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0 or action == 'delete':
        orderItem.delete()
    return JsonResponse('added', safe = False)

def cart(request):
    if request.user.is_authenticated: #kiểm tra xem user đã đăng nhập chưa
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context = {'categories': categories, 'items' : items, 'order': order, 'cartItems' : cartItems, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated: #kiểm tra xem user đã đăng nhập chưa
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub = False)
    context = {'categories': categories, 'items' : items, 'order': order, 'cartItems' : cartItems, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/checkout.html', context)

def search(request):
    if request.method == 'POST':
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated: #kiểm tra xem user đã đăng nhập chưa
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    products = Product.objects.all()
    context = {'keys': keys, 'searched': searched, 'items': items, 'cartItems': cartItems, 'products': products, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/search.html', context)

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        user_not_login = "hidden"
        user_login = "show"
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        user_not_login = "show"
        user_login = "hidden"
    context = {'form' : form, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        user_not_login = "hidden"
        user_login = "show"
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'user or password incorrect!')
    else:
        user_not_login = "show"
        user_login = "hidden"
    context = {'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories' : categories, 'active_category': active_category, 'products' : products}
    return render(request, 'app/category.html', context)

def detail(request):
    if request.user.is_authenticated: #kiểm tra xem user đã đăng nhập chưa
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id', '')
    categories = Category.objects.filter(is_sub = False)
    products = Product.objects.filter(id = id)
    context = {'categories': categories, 'products' : products, 'cartItems' : cartItems, 'user_not_login': user_not_login, 'user_login': user_login, 'items':items}
    return render(request, 'app/detail.html', context)
