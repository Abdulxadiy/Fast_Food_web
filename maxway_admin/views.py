from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from maxway_users.models import *
from . import services
from . import forms


def login_required_decorator(func):
    return login_required(func, login_url='login_page')


def login_page(request):
    if request.POST:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            return redirect("main_page")

    return render(request, 'maxway_admin/login.html')


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect("login_page")


@login_required_decorator
def main_dashboard(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    customers = Users.objects.all()
    orders = Order.objects.all()
    categories_products = []
    table_list=services.get_table()

    for category in categories:
        categories_products.append(
            {
                "category": category.name,
                "product": len(Product.objects.filter(category_id=category.id))
            }
        )

    ctx = {
        "counts": {
            "categories":len(categories),
            "products": len(products),
            "customers": len(customers),
            "orders": len(orders),

        },
        "categories_products": categories_products,
        "table_list": table_list,

    }
    return render(request, 'maxway_admin/index.html',ctx)


@login_required_decorator
def category_list(request):
    categories = Category.objects.all()
    ctx = {
        'categories':categories
    }
    return render(request, "maxway_admin/category/list.html",ctx)

@login_required_decorator
def product_list(request):
    products = Product.objects.all()
    ctx = {
        'products':products
    }
    return render(request, "maxway_admin/product/list.html", ctx)

@login_required_decorator
def user_list(request):
    users = Users.objects.all()
    ctx = {
        'users':users
    }
    return render(request, "maxway_admin/user/list.html",ctx)\

@login_required_decorator
def order_list(request):
    orders = Order.objects.all()
    ctx = {
        'orders':orders
    }
    return render(request, "maxway_admin/order/list.html",ctx)

@login_required_decorator
def user_create(request):
    model = Users()
    form = forms.UsersForm(request.POST or None, instance=model)

    if request.POST and form.is_valid():
        form.save()

        actions = request.session.get('user', [])
        actions += [f"You created user: {request.POST.get('first_name')} {request.POST.get('last_name')}"]
        request.session['actions'] = actions

        user_count = request.session.get('user_count', 0)
        user_count += 1
        request.session['user_count'] = user_count

        return redirect('user_list')
    ctx = {
        'model':model,
        'form': form
    }
    return render(request, 'maxway_admin/user/form.html',ctx)

@login_required_decorator
def user_edit(request, pk):
    model = Users.objects.get(pk=pk)
    form = forms.UsersForm(request.POST or None, instance=model)

    if request.POST and form.is_valid():
        form.save()

        actions = request.session.get('user', [])
        actions += [f"You edited user: {request.POST.get('first_name')} {request.POST.get('last_name')}"]
        request.session['actions'] = actions

        return redirect('user_list')
    ctx = {
        'model':model,
        'form': form
    }
    return render(request, 'maxway_admin/user/form.html',ctx)

@login_required_decorator
def user_delete(request,pk):
    model = Users.objects.get(pk=pk)
    user_name = model.first_name + " " + model.last_name
    model.delete()

    actions = request.session.get('user', [])
    actions += [f"You deleted user: {user_name}"]
    request.session['actions'] = actions

    return  redirect("category_list")

@login_required_decorator
def category_create(request):
    model = Category()
    form = forms.CategoryForm(request.POST or None, instance=model)

    if request.POST and form.is_valid():
        form.save()

        actions = request.session.get('category', [])
        actions += [f"You created category: {request.POST.get('name')}"]
        request.session['actions'] = actions

        category_count = request.session.get('category_count', 0)
        category_count += 1
        request.session['category_count'] = category_count

        return redirect('category_list')
    ctx = {
        'model':model,
        'form': form
    }
    return render(request, 'maxway_admin/category/form.html', ctx)

@login_required_decorator
def category_edit(request,pk):
    model = Category.objects.get(pk=pk)
    form = forms.CategoryForm(request.POST or None, instance=model)

    if request.POST and form.is_valid():
        form.save()

        actions = request.session.get('category', [])
        actions += [f"You edited category: {request.POST.get('name')}"]
        request.session['actions'] = actions

        return redirect('category_list')
    ctx = {
        'model':model,
        'form': form
    }
    return render(request, 'maxway_admin/category/form.html',ctx)

@login_required_decorator
def category_delete(request,pk):
    model = Category.objects.get(pk=pk)
    category_name = model.name
    model.delete()

    actions = request.session.get('category', [])
    actions += [f"You deleted category: {category_name}"]
    request.session['actions'] = actions

    return  redirect("category_list")

@login_required_decorator
def product_create(request):
    model = Product()
    form = forms.ProductForm(request.POST or None,request.FILES or None, instance=model)

    if request.POST and form.is_valid():
        form.save()

        actions = request.session.get('product', [])
        actions += [f"You created product: {request.POST.get('name')}"]
        request.session['actions'] = actions

        product_count = request.session.get('product_count', 0)
        product_count += 1
        request.session['product_count'] = product_count

        return redirect('product_list')
    ctx = {
        'model':model,
        'form': form
    }
    return render(request, 'maxway_admin/product/form.html', ctx)

@login_required_decorator
def product_edit(request,pk):
    model = Product.objects.get(pk=pk)
    form = forms.ProductForm(request.POST or None,request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        form.save()

        actions = request.session.get('product', [])
        actions += [f"You edited product: {request.POST.get('name')}"]
        request.session['actions'] = actions

        return redirect('product_list')
    ctx = {
        'model':model,
        'form': form
    }
    return render(request, 'maxway_admin/product/form.html', ctx)

@login_required_decorator
def product_delete(request,pk):
    model = Product.objects.get(pk=pk)
    product_name = model.name
    model.delete()

    actions = request.session.get('product', [])
    actions += [f"You deleted product: {product_name}"]
    request.session['actions'] = actions

    return  redirect("product_list")

@login_required_decorator
def customer_order_list(request,id):
    customer_orders = services.get_order_by_user(id=id)
    ctx = {
        'customer_orders': customer_orders
    }
    return render(request, "maxway_admin/customer_order/list.html", ctx)

@login_required_decorator
def order_product_list(request,id):
    order_products = services.get_product_by_order(id=id)
    ctx = {
        'order_products': order_products
    }
    return render(request, "maxway_admin/order_product/list.html", ctx)

@login_required_decorator
def profile(request):
    return render(request, 'maxway_admin/profile.html')