from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from django.http import JsonResponse

from demo.forms import RegisterUserForm
from demo.models import User, Order, Product, Cart, ItemInOrder, Category


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


def validate_username(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def validate_email(request):
    email = request.GET.get('email', None)
    response = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(response)


def about(request):
    products = Product.objects.filter(count__gte=1).order_by('-date')[:5]
    return render(request, 'demo/about.html', context={'products': products})


def contact(request):
    return render(request, 'demo/contact.html')


def catalog(request):
    category = request.GET.get('category')

    if category:
        products = Product.objects.filter(count__gte=1, category=category)
    else:
        products = Product.objects.filter(count__gte=1)
    order_by = request.GET.get('order_by')
    if order_by:
        products = products.order_by(order_by)
    else:
        products = products.order_by('-date')

    return render(request, 'demo/catalog.html', context={'category': Category.objects.all(), 'products': products})


def product(request, pk):
    item = Product.objects.get(pk=pk)

    return render(request, 'demo/product.html', context={'item': item})


@login_required
def cart(request):
    cart_items = request.user.cart_set.all()
    return render(request, 'demo/cart.html', context={'cart_items': cart_items})


@login_required
def checkout(request):
    password = request.GET.get('password', None)
    valid = request.user.check_password(password)
    if not valid:
        return JsonResponse({
            'error': 'Не верный пароль'
        })
    item_in_cart = request.user.cart_set.all()
    if not item_in_cart:
        return JsonResponse({
            'error': 'Корзина пуста'
        })
    order = Order.objects.create(user=request.user)
    for item in item_in_cart:
        ItemInOrder.objects.create(order=order, product=item.product, count=item.count, price=item.count * item.product.price)
    item_in_cart.delete()
    return JsonResponse({
        'message': 'Заказ оформлен'
    })


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'demo/orders.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-date')


@login_required
def delete_order(request, pk):
    order = Order.objects.filter(user=request.user, pk=pk, status='new')
    if order:
        order.delete()
    return redirect('orders')


@login_required
def to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item_in_cart = Cart.objects.filter(user=request.user, product=product).first()
    if item_in_cart:
        if item_in_cart.count + 1 > item_in_cart.product.count:
            return JsonResponse({
                'error': 'Невозможно добавить больше'
            })
        item_in_cart.count += 1
        item_in_cart.save()
        return JsonResponse({
            'count': item_in_cart.count
        })
    item_in_cart = Cart(user=request.user, product=product, count=1)
    item_in_cart.save()
    return JsonResponse({
        'count': item_in_cart.count
    })


def delete_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item_in_cart = Cart.objects.filter(user=request.user, product=product).first()
    if item_in_cart:
        if item_in_cart.count - 1 == 0:
            item_in_cart.delete()

            return JsonResponse({
                'count': 0
            })

    item_in_cart.count -= 1
    item_in_cart.save()
    return JsonResponse({
        'count': item_in_cart.count
    })
