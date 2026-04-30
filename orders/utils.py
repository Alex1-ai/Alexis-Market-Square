import threading
from django.core.mail import EmailMessage


import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY



def send_email_resend(to_email, subject, html_content):

    try:
        response = resend.emails.send({
            "from":"<onboarding@resend.dev>",
            "to": "alexanderemmanuel1719@gmail.com",
            "subject": subject,
            "html": "<p>Hello World<p>",
        })

        print("Resend response:", response)

    except Exception as e:
        print("Resend email error:", e)



def send_email_async(email):
    """Send email in a separate thread"""
    email.send(fail_silently=False)


def send_email(email):
    """Wrapper to run email in background"""
    thread = threading.Thread(target=send_email_async, args=(email,))
    thread.start()



def send_emails_async(email):
    def _send():
        try:
            email.send()
            # email.send()
            print("async emails sent ")
        except Exception as e:
            print("Email error:", e)

    threading.Thread(target=_send).start()
