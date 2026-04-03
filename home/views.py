from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Product, ReviewRating
from .forms import NewsletterSubscriptionForm, ContactForm
from .models import Features, FrequentQuestion, HomePageWords, NewsletterSubscription, Contact, SupportStaffDetails, Testimonies
from category.models import Market
from app.settings import ADMIN_EMAIL, DEBUG
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your views here.


def home(request):

    features = Features.objects.all()
    homeWords = HomePageWords.objects.all()[0]
    testimonies = Testimonies.objects.all()
    markets = Market.objects.all()
    staffDetails = SupportStaffDetails.objects.all()[0]
    # print(staffDetails.location, features, testimonies)
    faqs = FrequentQuestion.objects.all().order_by('number')

    # print(DEBUG)
    products = Product.objects.all().filter(
        is_available=True).order_by('-modified_date')

    reviews=None
    for product in products:
        reviews = ReviewRating.objects.filter(
            product_id=product.id, status=True)
    context = {
        'features': features,
        'homeWords': homeWords,
        'testimonies': testimonies,
        "staffDetails": staffDetails,
        "markets": markets,
        "faqs": faqs,
        'products': products,
        'reviews': reviews,

    }
    # print(markets)
    return render(request, 'index.html', context)

def markets(request):
    markets = Market.objects.all()

    context = {
        "markets": markets

    }
    return render(request, 'market.html', context)

def contact(request):
    if request.method == 'POST':
        # print("Entered")
        form = ContactForm(request.POST)
        # print("About to ")
        if form.is_valid():
            # print("Start")
            contact_name = form.cleaned_data['contact_name']
            # print("2")
            email = form.cleaned_data['email']
            # print("3")
            subject = form.cleaned_data['subject']
            # print("4")
            description = form.cleaned_data['description']
            # print("5")
            print(contact_name, description, email, subject)
            contact = Contact.objects.create(
                contact_name=contact_name, email=email, subject=subject, description=description)
            contact.save()
            # print("8")
            mail_subject = 'ALEXIS-MARKET-SQUARE CONTACT US MESSAGE'
            message = render_to_string(
                'accounts/contact_email.html', {
                    'user': contact,



                })
#             message = """
#                                     Hi Admin,
#                     Please some one just sent a message through contact us.
#                     user: {{ user}}


#                     If you think this is not for you, please ignore this email.

# """
            to_email = ADMIN_EMAIL
            # to_email = "alexanderemmanuel1719@gmail.com"
            send_email = EmailMessage(
                mail_subject,
                message,
                to=[to_email]
            )
            # print(mail_subject,message, to_email)
            # print("admin Email: ", ADMIN_EMAIL)
            try:
                send_email.send()
                # print("sent")
                messages.success(
                    request, "Thanks for reaching out to us, We would get back to you as soon as possible")
                return redirect('home')
            except:
                # print("error")
                messages.error(
                    request, "Please check your internet connectiona and try again!")
                return redirect('contact')

        else:
            # print("correct credentials")
            messages.error(
                request, "All the credentials are required and must be valid.")
            return redirect('contact')
    else:
        return render(request, 'contact.html')


def newsletter(request):
    # print(" this is the path", path)
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            subcriber = NewsletterSubscription.objects.create(email=email)
            subcriber.save()
            mail_subject = 'ALEXIS-MARKET-SQUARE SUBSCRIPTION MESSAGE'
            message = f"Hi Admin,\nPlease some one just Subscribed to our newssletter."
            to_email = ADMIN_EMAIL
            send_email = EmailMessage(
                mail_subject,
                message,
                to=[to_email]
            )
            try:
                send_email.send()
                messages.success(
                    request, 'Thanks for subscribing to our newsletter!')

            except:
                messages.error(
                    request, "Could Not Subscribe you. Please check your internet connectiona and try again!")
            # Redirect to a success page

    return redirect(request.META.get('HTTP_REFERER'))
