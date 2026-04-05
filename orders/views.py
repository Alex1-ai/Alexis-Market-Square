from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import datetime
from store.models import Product
from django.core.mail import EmailMessage
from app.settings import ADMIN_EMAIL
import json
# Create your views here.
from django.template.loader import render_to_string
import json
from app.settings import STANDARD_DELIVERY
from django.urls import reverse
import logging
logger = logging.getLogger(__name__)



def payments(request):
    # PayPal sends JSON; Pay-on-Delivery sends a regular form POST
    if request.content_type == 'application/json':
        body = json.loads(request.body)
        order_id       = body['orderID']
        trans_id       = body['transID']
        payment_method = body['payment_method']
        status         = body['status']
    else:
        logger.info("payments on delivery view started")
        order_id       = request.POST.get('orderID')
        trans_id       = 'POD-' + order_id  # no real transaction ID for cash
        payment_method = request.POST.get('payment_method')
        status         = 'PENDING'
    logger.info("payments view started")
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=order_id
    )

    payment = Payment(
        user=request.user,
        payment_id=trans_id,
        payment_method=payment_method,
        amount_paid=order.order_total,
        status=status
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    logger.info("order saved")
    # Move cart items to OrderProduct table
    logger.info("cart items processed")
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id      = order.id
        orderproduct.payment       = payment
        orderproduct.user_id       = request.user.id
        orderproduct.product_id    = item.product_id
        orderproduct.quantity      = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered       = True
        orderproduct.save()

        cart_item      = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct   = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        product        = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    CartItem.objects.filter(user=request.user).delete()
    try:
        # Admin email
        mail_subject = 'ALEXIS-MARKET-SQUARE ORDER MESSAGE'
        message      = 'Hi Admin,\nSomeone just placed an order.'
        EmailMessage(mail_subject, message, to=[ADMIN_EMAIL]).send(fail_silently=True)
        logger.info("emails sent")
        # Customer email
        mail_subject = 'Order Successful!'
        message = render_to_string('orders/order_received_email.html', {
            'user': request.user,
            'order': order,
        })

        logger.info("emails sent")
        EmailMessage(mail_subject, message, to=[request.user.email]).send(fail_silently=True)
        logger.info("emails sent")
    except Exception as e:
        print("Error sending email:", e)
    # ── Different response for each payment type ──
    if request.content_type == 'application/json':
        # PayPal: JavaScript fetch() expects JSON back
        return JsonResponse({
            'order_number': order.order_number,
            'transID': payment.payment_id
        })
    else:
        logger.info("emails sent 2")
        # Pay on Delivery: normal redirect
        url = reverse('order_complete')
        return redirect(
            f"{url}?order_number={order.order_number}&payment_id={payment.payment_id}"
        )


# def payments(request):
#     body = json.loads(request.body)
#     print("here is the body",body)
#     order = Order.objects.get(
#         user=request.user, is_ordered=False, order_number=body['orderID'])

#     # print(body)
#     # store transaction detials into payment model
#     payment = Payment(
#         user=request.user,
#         payment_id=body['transID'],
#         payment_method=body['payment_method'],
#         amount_paid=order.order_total,
#         status=body['status']
#     )
#     payment.save()
#     order.payment = payment
#     order.is_ordered = True
#     order.save()
#     #print("Ordered successfully")

#     # Move the cart items to Order Product table
#     cart_items = CartItem.objects.filter(user=request.user)

#     for item in cart_items:
#         #print("1 part")
#         orderproduct = OrderProduct()
#         #print("2 part")
#         orderproduct.order_id = order.id
#         #print("3 part")
#         orderproduct.payment = payment
#        # print("4 part")
#         orderproduct.user_id = request.user.id
#        # print("5 part")
#         orderproduct.product_id = item.product_id
#        # print("6 part")
#         orderproduct.quantity = item.quantity
#        # print("7 part")
#         orderproduct.product_price = item.product.price
#        # print("8 part")
#         orderproduct.ordered = True
#        # print("9 part")
#         orderproduct.save()
#        # print("2 seconds")
#         cart_item = CartItem.objects.get(id=item.id)
#         #print("10 part")
#         product_variation = cart_item.variations.all()
#         #print("11 part")
#         #print(f"product_variation: {product_variation} ")
#         orderproduct = OrderProduct.objects.get(id=orderproduct.id)
#         orderproduct.variations.set(product_variation)
#         orderproduct.save()

#     # Reduce the quantity of the
#         product = Product.objects.get(id=item.product_id)
#         product.stock -= item.quantity
#         product.save()

#     # clear cart
#     CartItem.objects.filter(user=request.user).delete()

#     # send email notification to the admin
#     mail_subject = 'ALEXIS-MARKET-SQUARE ORDER MESSAGE'
#     message = f"Hi Admin,\nPlease some one just Someone just placed an order Now."
#     to_email = ADMIN_EMAIL
#     admin_email = EmailMessage(
#         mail_subject,
#         message,
#         to=[to_email]
#     )
#     admin_email.send()
#     # send order received email to customer
#     mail_subject = 'Order Successful!'
#     message = render_to_string(
#         'orders/order_received_email.html', {
#             'user': request.user,
#             'order': order,

#         })
#     to_email = request.user.email
#     send_email = EmailMessage(
#         mail_subject,
#         message,
#         to=[to_email]
#     )
#     send_email.send()

#     # send ordernumber and transaction id back to sendData method using javascript
#     data = {
#         'order_number': order.order_number,
#         'transID': payment.payment_id
#     }

#     return JsonResponse(data)
    # return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # if the cart count is less than or equal to 0, the redirect back to shop
    # cart_items = CartItem.objects.filter(user=current_user)
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    #standard_delivery = 5
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    # grand_total = total + tax + STANDARD_DELIVERY
    grand_total = total

    if request.method == 'POST':
        print("Entering the form")
        payment_type = request.POST.get('payment_method')
        print("Payment method is:", payment_type)
        form = OrderForm(request.POST)
        print("Creeating an instance of the form")
        if form.is_valid():
            print("Enter is valid")
            # store all the billing information include order table
            data = Order()
            print("num 1")
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generating an order id
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'standard_delivery': STANDARD_DELIVERY,
                'payment_type': payment_type,
                'grand_total': grand_total
            }
            return render(request, 'orders/payments.html', context)
        else:
            print("Failed")
            return redirect('home')
    else:
        return redirect('checkout')


def order_complete(request):

    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            'standard_delivery': STANDARD_DELIVERY
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
