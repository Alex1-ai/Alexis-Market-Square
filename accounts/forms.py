from django import forms
from .models import Account, UserProfile
import re


class RegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': ' Enter Password',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': ' Confirm Password',

    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegisterationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
            self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
            self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

            self.fields[field].widget.attrs['class'] = 'form-control text-dark'
            # self.fields[field].widget.attrs['class'] = 'text-black'

    def clean(self):
        cleaned_data = super(RegisterationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        has_lowercase = False
        has_uppercase = False
        has_number = False
        has_symbol = False

        # Loop through each character in the password
        for char in password:
            if char.islower():
                has_lowercase = True
            elif char.isupper():
                has_uppercase = True
            elif char.isdigit():
                has_number = True
            else:
                has_symbol = True
        # VALIDATION STARTS HERE
        if len(password) < 8:
            raise forms.ValidationError(
                "Password must not be less than eight characters!"
            )

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match!"
            )

            # Check if all categories are satisfied
        if not has_lowercase:
            raise forms.ValidationError(
                "Password must contain at least one symbol, number, uppercase and  lowercase letter.")
        if not has_uppercase:
            raise forms.ValidationError(
                "Password must contain at least one symbol, number, uppercase and  lowercase letter.")
        if not has_number:
            raise forms.ValidationError(
                "Password must contain at least one symbol, number, uppercase and  lowercase letter.")
        if not has_symbol:
            raise forms.ValidationError(
                "Password must contain at least one symbol, number, uppercase and  lowercase letter.")


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("first_name", "last_name", "phone_number")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control text-dark'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={
                                       'invlaid': ("image file only ")}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2',
                  'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control text-dark'
