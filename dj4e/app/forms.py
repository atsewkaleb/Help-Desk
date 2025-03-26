from django import forms
from .models import Request
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'role', 'first_name', 'last_name', 'username', 'location', 'department', 'phone',  'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user






class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['request_type']


class ReqeustEditClient(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['feed_back']

class ReqeustEditStaff(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['is_completed']




User = get_user_model()

class RequestEditForm(forms.ModelForm):
    assigned_team_leader = forms.ModelChoiceField(
        queryset=User.objects.filter(role='team_leader'),
        required=False,
        empty_label="Select a team leader",
        label="Assigned Team Leader"
    )
    assigned_staff = forms.ModelChoiceField(
        queryset=User.objects.filter(role='staff'),
        required=False,
        empty_label="Select a staff member",
        label="Assigned Staff"
    )
    class Meta:
        model = Request
        fields = ['is_approved', 'assigned_team_leader', 'assigned_staff', 'is_completed']
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['assigned_team_leader'].label_from_instance = lambda obj: obj.email
         self.fields['assigned_staff'].label_from_instance = lambda obj: obj.email

