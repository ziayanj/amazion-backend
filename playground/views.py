from django.core.mail import send_mail, mail_admins, EmailMessage, BadHeaderError
from django.shortcuts import render
from django.db.models import Q, F, Func, Value, Count, ExpressionWrapper, DecimalField, IntegerField, FloatField, BooleanField
from django.db.models.aggregates import Min, Sum, Max, Avg
from django.db.models.functions import Concat, Cast
from django.contrib.contenttypes.models import ContentType
from django.db import transaction, connection
import requests
from templated_mail.mail import BaseEmailMessage
from store.models import Product, OrderItem, Order, Customer, Collection, Cart, CartItem
from tags.models import TaggedItem
from .tasks import notify_customers

@transaction.atomic()
def say_hello(request):
    requests.get('https://httpbin.org/delay/2')
    # notify_customers.delay('Hello')

    # try:
        # send_mail('subject', 'message', 'from@amazion.com', ['to@amazion.com'])
        # mail_admins('subject', 'old message', html_message='<h1>message</h1>')

        # message = EmailMessage('subject', 'message', 'from@amazion.com', ['to@amazion.com'])
        # message.attach_file('playground/static/images/boon.png')
        # message.send()

    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Test Name'}
    #     )
    #     message.send(['to@amazion.com'])
    # except BadHeaderError:
    #     pass
    # ordered_products = OrderItem.objects.values_list('product_id').distinct()

    # queryset = Product.objects.filter(id__in=ordered_products).order_by('title')

    # queryset = Product.objects.select_related('collection').prefetch_related('promotions').all()
    queryset = Collection.objects.annotate(
        products_count=Count('products')
    )

    # for i in list(queryset):
    #     print(i.products_count)

    # haha = Customer.objects.annotate(
    #     new_id=F('id'),
    #     full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    # )

    # okay = Order.objects.aggregate

    # haha = Customer.objects.annotate(
    #     new_id=F('id'),
    #     full_name=Concat('first_name', Value(' '), 'last_name'),
    #     orders_count=Count(F('order')),
    #     last_order=Max('order__id')
    # )

    # col = Collection.objects.annotate(
    #     products_count=Count(F('product'))
    # )

    # asd = ExpressionWrapper(Count(F('order')) > 5, output_field=BooleanField())

    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # print(asd)

    # col = Customer.objects \
    #     .annotate(orders_count=Count(F('order'))) \
    #     .filter(orders_count__gt=5)

    # col = Customer.objects.annotate(
    #     spent_amount=Sum(F('order__orderitem__unit_price') * F('order__orderitem__quantity'))
    # )

    # col = Product.objects \
    #     .annotate(total_sales=Sum(F('orderitem__unit_price') * F('orderitem__quantity'))) \
    #     .order_by(F('total_sales').desc(nulls_last=True))[:5]

    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # ok = Product.objects.annotate(
    #     discounted_price=discounted_price
    # )

    # queryset = TaggedItem.objects.get_tags_for(Product, 1)

    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()

    # collection = Collection.objects.filter(pk=11).update(featured_product=None)

    # cart = Cart.objects.create()

    # cart_item = CartItem()
    # cart_item.cart = cart
    # cart_item.product = Product(pk=1)
    # cart_item.quantity = 1
    # cart_item.save()

    # print(cart)
    # print(cart.id)
    # print(cart_item)
    # print(cart_item.id)

    # item = CartItem.objects.filter(pk=1).update(quantity=F('quantity') + 1)

    # Cart.objects.get(pk=1).delete()

    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    # with connection.cursor() as cursor:
    #     print(cursor.execute('SELECT * FROM store_product'))

    # sad = Order.objects.aggregate(Count('id'))
    # sad = OrderItem.objects.filter(product_id=1, order__payment_status='C').aggregate(Sum('quantity'))
    # sad = Order.objects.filter(customer_id=1).aggregate(Count('id'))
    # sad = Product.objects.filter(collection__id=3).aggregate(Min('unit_price'), Max('unit_price'), Avg('unit_price'))
    # print(sad)

    # orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    
    # items = OrderItem.objects.select_related('product').filter(order_id__in=[i.id for i in orders])

    # print(orders)
    # print(items)

    # print(queryset[0])
    # print(queryset[0]['title'])
    # print(queryset[0]['unit_price'])

    # return render(request, 'hello.html', { 'name': 'Ziayan', 'tags': list(queryset) })
    return render(request, 'hello.html', { 'name': 'Ziayan' })
