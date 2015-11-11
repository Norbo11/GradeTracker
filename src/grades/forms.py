from datetime import date
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from grades.models import StudiedSubject


DAYS = list()
for day in range(1, 32):
    day = str(day) if day >= 10 else '0' + str(day)
    DAYS.append((day, day))

MONTHS = list()
for month in range(1, 13):
    month = str(month) if month >= 10 else '0' + str(month)
    MONTHS.append((month, month))

YEARS = list()
for year in range(1900, date.today().year - 15):
    year = str(year)
    YEARS.append((year, year))

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if (fieldname == "email"): field.widget.attrs['placeholder'] = 'E-Mail'
            if (fieldname == "username"): field.widget.attrs['placeholder'] = 'Username'
            if (fieldname == "password1"): field.widget.attrs['placeholder'] = 'Password'
            if (fieldname == "password2"): field.widget.attrs['placeholder'] = 'Confirm Password'

    email = forms.EmailField(max_length=100)
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    dob_day = forms.ChoiceField(choices=(DAYS))
    dob_month = forms.ChoiceField(choices=(MONTHS))
    dob_year = forms.ChoiceField(choices=(YEARS))

    def clean(self):
        if (self.cleaned_data.get('password1') != self.cleaned_data.get('password2')):
            raise ValidationError("Passwords do not match.")

        return self.cleaned_data

class AddSubjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddSubjectForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = StudiedSubject
        fields = ['subject', 'teacher1', 'teacher2']
