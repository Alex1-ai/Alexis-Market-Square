# orders/tasks.py
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from app.settings import ADMIN_EMAIL



@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_emails(self, user_id, order_id):
    """Send admin + customer order confirmation emails asynchronously."""
    print(ADMIN_EMAIL)
    from django.contrib.auth import get_user_model
    from .models import Order

    User = get_user_model()
    try:
        print("fetching data from database")
        user  = User.objects.get(id=user_id)
        order = Order.objects.select_related('payment').get(id=order_id)
        print("Sending gmail")
        # Admin notification
        EmailMessage(
            'ALEXIS-MARKET-SQUARE ORDER MESSAGE',
            'Hi Admin,\nSomeone just placed an order.',
            to=[ADMIN_EMAIL]
        ).send()
        # ).send(fail_silently=True)

        # Customer confirmation
        message = render_to_string('orders/order_received_email.html', {
            'user': user,
            'order': order,
        })
        # print("sending gmail to customer")
        EmailMessage(
            'Order Successful!',
            message,
            to=[user.email]
        ).send()
        # ).send(fail_silently=True)
        # print("email sent successfully")
    except Exception as exc:
        print("Error sending email:", exc)
        raise self.retry(exc=exc)
