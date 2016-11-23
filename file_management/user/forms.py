from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.forms.widgets import FileInput

# from user.models import UserProfile
#
#
# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=100, required=True,
#                                error_messages={'required': "You must provide a username."})
#     password = forms.CharField(max_length=32, widget=forms.PasswordInput, required=True,
#                                error_messages={'required': "You must provide a password."})
#
#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#
#         if username is None or password is None:
#             pass
#         else:
#             user = authenticate(username=username, password=password)
#             if user is None:
#                 self.add_error(None, "Invalid login.")
#             else:
#                 self.fields['user'] = user
