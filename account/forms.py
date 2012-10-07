from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from account.models import UserProfile
from captcha.fields import CaptchaField

class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label="Nama Depan")
    last_name = forms.CharField(max_length=30, required=False, label="Nama Belakang")
    email = forms.EmailField(required=False, label="Alamat E-Mail")
    is_superuser = forms.BooleanField(required=False, label="Admin?")
    is_staff = forms.BooleanField(required=False, label="Staff?")
    
    error_css_class = "alert alert-error"
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_superuser = self.cleaned_data["is_superuser"]
        user.is_staff = self.cleaned_data["is_staff"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, label="Nama Depan (boleh kosong)",
    )
    last_name = forms.CharField(
        max_length=30, required=False, label="Nama Belakang (boleh kosong)",
    )
    email = forms.EmailField(label="Alamat E-Mail (wajib)")
    address = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label = "Alamat Rumah (boleh kosong)",
    )
    phone = forms.CharField(
        required = False,
        label = "Nomor Telpon/HP (boleh kosong)",
    )
    captcha = CaptchaField()
    
    error_css_class = "alert alert-error"
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",
                "password1", "password2")
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False, label="Nama Depan")
    last_name = forms.CharField(max_length=30, required=False, label="Nama Belakang")
    email = forms.EmailField(label="Alamat E-Mail")
    address = forms.CharField(widget=forms.Textarea, required=False)
    phone = forms.CharField(required=False)
    
    error_css_class = "alert alert-error"
    error_messages = {
        'invalid_user': "Username tidak boleh kosong",
    }
    
    def __init__(self, *args, **kwargs):
        self.logged_user = kwargs.pop('logged_user', None)
        self.user_profile = kwargs.pop('user_profile', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
    
    def save_user(self, commit=True):
        if self.logged_user == None:
            raise form.ValidationError(self.error_messages['invalid_user'])
        
        self.logged_user.first_name = self.cleaned_data["first_name"]
        self.logged_user.last_name = self.cleaned_data["last_name"]
        self.logged_user.email = self.cleaned_data["email"]
        
        if commit:
            self.logged_user.save()
        return self.logged_user

    def save_profile(self, commit=True):
        if self.user_profile == None:
            raise form.ValidationError(self.error_messages['invalid_user'])
        
        self.user_profile.address = self.cleaned_data["address"]
        self.user_profile.phone = self.cleaned_data["phone"]

        if commit:
            self.user_profile.save()
            
        return self.user_profile

