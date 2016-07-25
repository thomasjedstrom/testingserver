from django import forms

class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		widgets = {
		'password': forms.PasswordInput(),
		}