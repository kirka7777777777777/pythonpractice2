from .models import UserProfile  # Оставьте другие импорты, которые вам нужны
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import ImageUpload
from django.core.exceptions import ValidationError
from django.conf import settings


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20, required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user, phone_number=self.cleaned_data.get('phone_number'))
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserProfileViewForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['title', 'image']



class ApplicationForm(forms.Form):
    CATEGORY_CHOICES = [  # Определите список категорий как кортеж кортежей
        ('3d_design', '3D-дизайн'),
        # Используйте значения, подходящие для хранения в базе данных (без пробелов, строчные буквы)
        ('2d_design', '2D-дизайн'),
        ('sketch', 'Эскиз'),
        ('other', 'Другое'),  # Добавьте свои категории
    ]

    title = forms.CharField(
        label='Название',
        max_length=255,
        widget=forms.TextInput(attrs={'required': 'required'})
    )
    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={'required': 'required'})
    )
    category = forms.ChoiceField(  # <--- ИСПОЛЬЗУЙТЕ ChoiceField ВМЕСТО ModelChoiceField
        label='Категория',
        choices=CATEGORY_CHOICES,  # <--- Укажите список категорий choices
        widget=forms.Select(attrs={'required': 'required'})
    )
    photo = forms.ImageField(
        label='Фото помещения или план',
        widget=forms.FileInput(attrs={'required': 'required'})
    )

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            max_size = 2 * 1024 * 1024  # 2MB в байтах
            if photo.size > max_size:
                raise ValidationError(f"Размер изображения не должен превышать {max_size / (1024 * 1024)} Мб.")

            allowed_formats = ['jpg', 'jpeg', 'png', 'bmp']
            file_extension = photo.name.split('.')[-1].lower()
            if file_extension not in allowed_formats:
                raise ValidationError(f"Поддерживаемые форматы изображений: {', '.join(allowed_formats)}.")
        return photo

