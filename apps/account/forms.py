from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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
		fields = ('username', 'email', 'password1', 'password2', 'profile_photo')

	def __init__(self, *args, **kwargs) -> None:
		super(RegistrationForm,self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Enter Username'})
		self.fields['email'].widget.attrs.update({'class':'form-control','placeholder':'Enter email'})
		self.fields['password1'].widget.attrs.update({'class':'form-control','placeholder':'Enter password'})
		self.fields['password2'].widget.attrs.update({'class':'form-control','placeholder':'Enter password confirmation'})
		self.fields['profile_photo'].widget.attrs.update({'class':'form-control','placeholder':'Chouse avatar'})

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
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

