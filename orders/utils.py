import threading
from django.core.mail import EmailMessage


def send_email_async(email):
    """Send email in a separate thread"""
    email.send(fail_silently=False)


def send_email(email):
    """Wrapper to run email in background"""
    thread = threading.Thread(target=send_email_async, args=(email,))
    thread.start()



def send_emails_async(admin_email, customer_email):
    def _send():
        try:
            admin_email.send()
            customer_email.send()
        except Exception as e:
            print("Email error:", e)

    threading.Thread(target=_send).start()
