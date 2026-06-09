import json
from decimal import Decimal
from django.db import transaction
from .models import Users, Order, OrderProduct
from django.shortcuts import render
from django.http import JsonResponse
from maxway_users.models import Category, Product

def home_page(request):
    product_id = request.GET.get('product_id')
    if product_id:
        try:
            product_id = int(product_id)
            product = Product.objects.get(id=product_id)
            data = {
                'price': str(product.price),
                'image': product.image.name if product.image else '',
                'name': product.name,
                'description': product.description or ''
            }
            return JsonResponse(data)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    categories = Category.objects.all()
    products = Product.objects.all()
    ctx = {
        'categories': categories,
        'products': products
    }
    return render(request, 'maxway_users/index.html', ctx)


def order_page(request):
    ctx_user = {}

    if request.method == 'POST':
        phone = request.POST.get('phone')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        payment_type = request.POST.get('payment_type')
        address = request.POST.get('address')

        user, created = Users.objects.get_or_create(
            phone=phone,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'address': address,
            }
        )

        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.address = address
            user.save()

        try:
            cart_j = json.loads(request.POST.get('cart_items', '{}'))

            if not cart_j:
                return JsonResponse({'error': 'Cart is empty'}, status=400)
            with transaction.atomic():
                order = Order.objects.create(
                    status=0,
                    payment_type=payment_type,
                    address=address,
                    customer=user
                )
                for product_id, item in cart_j.items():
                    try:
                        product = Product.objects.get(id=int(product_id))

                        OrderProduct.objects.create(
                            count=int(item['qty']),
                            price=Decimal(str(item['price'])),
                            product=product,
                            order=order
                        )

                    except Product.DoesNotExist:
                        return JsonResponse({'error': f'Product {item["name"]} not found'}, status=404)

            # Order created successfully
            return JsonResponse({
                'success': True,
                'message': 'Buyurtma muvaffaqiyatli yaratildi!',
                'order_id': order.id
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid cart data'}, status=400)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        phone = request.GET.get('phone', '')
        try:
            user = Users.objects.get(phone=phone)
            return JsonResponse({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'address': user.address,
            })
        except Users.DoesNotExist:
            return JsonResponse({})

    return render(request, 'maxway_users/order.html')
