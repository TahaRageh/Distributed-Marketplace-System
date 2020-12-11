from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from.models import *
from.forms import CreateUserForm, ProductForm



def registerPage(response):
    if response.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if response.method == "POST":
            form = CreateUserForm(response.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(response, "Account was created for "+user)
                return redirect('login')
        return render(response, 'app/register.html', {'form': form})

def loginPage(response):
    if response.user.is_authenticated:
        return redirect('home')
    else:
        if response.method == "POST":
            username = response.POST.get('username')
            password = response.POST.get('password')
            user = authenticate(response, username=username, password=password)
            if user is not None:
                login(response, user)
                return redirect('home')
            else:
                messages.info(response, "Username Or Password is incorrect")
        return render(response, 'app/login.html')

def logoutUser(response):
    logout(response)
    return redirect('login')


def home(request):
    products = Product.objects.filter(status=True)
    return render(request, 'app/home.html', {"products": products})


def product_detail(request, id):
    if request.method == 'POST' and not request.user.is_anonymous() and \
        Purchase.objects.filter(product_id=id, buyer=request.user).count() > 0 and \
        'content' in request.POST and request.POST['content'].strip() != '':
            Review.objects.create(content=request.POST['content'], product_id=id, user=request.user)

    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return redirect('/')

    if request.user.is_anonymous() or \
        Purchase.objects.filter(product=product, buyer=request.user).count() == 0 or \
        Review.objects.filter(product=product, user=request.user).count() > 0:
            show_post_review = False
    else:
        show_post_review = Purchase.objects.filter(product=product, buyer=request.user).count() > 0

    reviews = Review.objects.filter(product=product)
    # Generate client token to handle payments
    #client_token = braintree.ClientToken.generate()
    return render(request, 'app/product_detail.html', {"product": product, "show_post_review": show_post_review, "reviews": reviews})


@login_required(login_url='login')
def create_product(request):
    error = ''
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('my_products')
        else:
            error = "Data is not valid"

    product_form = ProductForm()
    return render(request, 'app/create_product.html', {"error": error})


@login_required(login_url='login')
def edit_product(request, id):
    try:
        product = Product.objects.get(id=id, user=request.user)
        error = ''
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES, instance=product)

            if product_form.is_valid():
                product.save()
                return redirect('my_products')
            else:
                error = "Data is nit valid"
        return render(request, 'app/edit_product.html', {"product": product, "error": error})
    except Product.DoesNotExist:
        return redirect('login')


@login_required(login_url='login')
def my_products(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'app/my_products.html', {"products": products})


@login_required(login_url='login')
def profile(request, username):
    if request.method == 'POST':  # Edit the profile page
        profile = Profile.objects.get(user=request.user)
        profile.about = request.POST['about']
        profile.slogan = request.POST['slogan']
        profile.save()
    else:
        try:  # Display the profile page
            profile = Profile.objects.get(user=Profile.user)
        except Profile.DoesNotExist:
            return redirect('profile')

    products = Product.objects.filter(user=profile.user, status=True)
    return render(request, 'app/profile.html', {"profile": profile, "products": products})

@login_required(login_url="login")
def save_avatar(backend, user, response, *args, **kwargs):
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        profile = Profile(user_id=user.id)

    profile.save()
@login_required(login_url="login")
def make_purchase(request):
    if request.method == 'POST' and request.user.is_anonymous():
        try:
            product = Product.objects.get(id=request.POST['product_id'])
        except Product.DoesNotExist:
            return redirect('login')

        #nonce = request.POST["payment_method_nonce"]
        #result = braintree.Transaction.sale({
           # "amount": product.price,
            #"payment_method_nonce": nonce
        #})

        #if result.is_success:
         #   Purchase.objects.create(product=product, buyer=request.user)

    return redirect('login')


@login_required(login_url="login")
def my_sales(request):
    purchases = Purchase.objects.filter(product__user=request.user)
    return render(request, 'app/my_sales.html', {"purchases": purchases})


@login_required(login_url="login")
def my_purchases(request):
    purchases = Purchase.objects.filter(buyer=request.user)
    return render(request, 'app/my_purchases.html', {"purchases": purchases})


def category(request, link):
    categories = {
        "Electronics": "EL",
        "Clothes": "CL",
        "sports": "SP",
        "appliances": "AP",
        "toys": "TY"
    }
    try:
        products = Product.objects.filter(category=categories[link])
        return render(request, 'app/home.html', {"products": products})
    except KeyError:
        return redirect('home')


def search(request):
    products = Product.objects.filter(title__contains=request.GET['title'])
    return render(request, 'app/home.html', {"products": products})

