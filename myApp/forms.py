from datetime import date
from django import forms,template
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs = {'autofocus': True})
    )

    birth_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = date.today()
        max_year = today.year - 16
        years_range = range(max_year, 1989, -1)

        self.fields['birth_date'].widget = forms.SelectDateWidget(
            years=years_range,
            empty_label=("Year", "Month", "Day")
            )
        self.fields['birth_date'].required = True

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        age = (date.today() - birth_date).days / 365.25
        if age < 16:
            raise forms.ValidationError("Sorry, you must be at least 16 years old to register.")
        return birth_date
        
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'birth_date', 'email', 'user_name', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']