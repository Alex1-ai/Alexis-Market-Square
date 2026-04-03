from django import forms
from .models import NewsletterSubscription, Contact


class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ('email',)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('contact_name', 'email', 'subject', 'description')
