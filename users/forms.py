from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, BaseInlineFormSet
from users.models import Profile, Activity, ProfileActivity
from locations.models import City
from django.core.exceptions import ValidationError




class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control",
            }
        ),
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control",
            }
        ),
    )
    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "data-toggle": "password",
                "id": "password",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control",
                "data-toggle": "password",
                "id": "password",
            }
        ),
    )


    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
       
            
            
        ]
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
            }
        ),
    )
    password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "data-toggle": "password",
                "id": "password",
                "name": "password",
            }
        ),
    )
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ["username", "password", "remember_me"]



class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False)
    telephone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    hide_email = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    hide_telephone = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'city', 'date_of_birth', 'telephone', 'hide_email', 'hide_telephone']



class ProfileActivityForm(forms.ModelForm):
    class Meta:
        model = ProfileActivity
        fields = ['activity', 'skill_level']
        widgets = {
            'activity': forms.Select(attrs={'class': 'form-control'}),
            'skill_level': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)  # Get the profile instance, default to None
        super().__init__(*args, **kwargs)

        if profile:
            # Get already chosen activities
            chosen_activities = ProfileActivity.objects.filter(profile=profile).values_list('activity_id', flat=True)
            # Exclude chosen activities from the queryset
            self.fields['activity'].queryset = Activity.objects.exclude(id__in=chosen_activities)

class ProfileActivityFormSet(BaseInlineFormSet):
    def __init__(self, *args, profile=None, **kwargs):
        super().__init__(*args, **kwargs)

        if profile:
            # Get already chosen activities
            chosen_activities = ProfileActivity.objects.filter(profile=profile).values_list('activity_id', flat=True)
            # Update the queryset for each form's activity field
            for form in self.forms:
                if hasattr(form, 'fields') and 'activity' in form.fields:
                    form.fields['activity'].queryset = Activity.objects.exclude(id__in=chosen_activities)

ProfileActivityFormSet = inlineformset_factory(Profile, ProfileActivity, form=ProfileActivityForm, formset=ProfileActivityFormSet, extra=1)