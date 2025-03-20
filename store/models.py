from django.db import models


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)

    # Example of handling Circular Dependancy
    featured_product = models.ForeignKey(
        'Product',                  # Refer the name as string, when class declared after the current
        on_delete=models.SET_NULL,  # If product deleted, set to null
        null=True,
        related_name='+',           # This tells Django, not to create reverse relationship
    )


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    
    # Creating many-to-one (many products to one collection) relationship
    collection = models.ForeignKey(
        Collection,                 # One collection has many products
        on_delete=models.PROTECT,   # If collection is deleted (accidentally), the products remain in the DB.
    )

    # Creating many-to-many relationship (many promotions to many products, and vice versa)
    promotions = models.ManyToManyField(Promotion)  # Use plural for the variable


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, 
        choices=MEMBERSHIP_CHOICES, 
        default=MEMBERSHIP_BRONZE
    )


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, 
        choices=PAYMENT_STATUS_CHOICES, 
        default=PAYMENT_STATUS_PENDING
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,   # The orders remain in the DB, even when the customer is deleted.
    )


class OderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )
    quantity = models.PositiveSmallIntegerField()   # Prevents negative numbers
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    # Creating one-to-one relationship
    # One customer has one address
    # customer = models.OneToOneField(
    #     Customer,                   # Parent model.
    #     on_delete=models.CASCADE,   # Remove the address when the customer is deleted.
    #     primary_key=True,           # Ensure one-to-one relationship. One customer has one address.
    # )

    # Creating one-to-many relationship
    # One customer has multiple addresses
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField()
