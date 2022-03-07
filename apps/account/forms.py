from django.contrib import messages
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


from apps.account.models import Account


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	profile_photo = forms.ImageField()
	error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
	password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
		help_text=password_validation.password_validators_help_text_html(),
	)
	password2 = forms.CharField(
		label=_("Password confirmation"),
		widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
		strip=False,
		help_text=_("Enter the same password as before, for verification."),
	)

	class Meta(UserCreationForm.Meta):
		model = Account
		fields = ('username', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs) -> None:
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Enter Username'})
		self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'Enter email'})
		self.fields['password1'].widget.attrs.update({'class':'form-control','placeholder':'Enter password'})
		self.fields['password2'].widget.attrs.update({'class':'form-control','placeholder':'Enter password confirmation'})

	def clean_username(self):
		username = self.cleaned_data['username']
		if Account.objects.filter(username=username).exists():
			raise forms.ValidationError("Username already exists")
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if Account.objects.filter(email=email).exists():
			raise forms.ValidationError("Email already exists")
		return email

	def clean(self):
		form_data = self.cleaned_data
		if form_data['password1'] != form_data['password2']:
			self._errors["password2"] = ["Password do not match"] # Will raise a error message
			del form_data['password2']
		return form_data

	def save(self, commit = True):  
		user = Account.objects.create(  
			self.cleaned_data['username'],  
			self.cleaned_data['email'],  
			self.cleaned_data['password1']
		)  
		return user

class UserForm(AuthenticationForm):
	password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

	error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }
	class Meta:
		model = Account
		fields = ('username', 'password')
	def __init__(self, *args, **kwargs):
		super(UserForm,self).__init__(*args,**kwargs)
		self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Username'})
		self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Password'})

