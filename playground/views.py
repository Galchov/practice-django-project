from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order, OrderItem

def say_hello(request):
    # Customers with '.com' ending emails
    # queryset = Customer.objects.filter(email__icontains='.com')

    # Collections that don't have a featured product
    # queryset = Collection.objects.filter(featured_product__isnull=True)

    # Products with low inventory
    # queryset = Product.objects.filter(inventory__lt=10)

    # Order, placed by customer with id = 1
    # queryset = Order.objects.filter(customer__id=1)

    # Order items for products in collection 3
    queryset = OrderItem.objects.filter(product__collection__id=3)

    return render(request, 'hello.html', {'name': 'Raymond', 'products': list(queryset)})
