from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Contact


class CustomFileInput(forms.ClearableFileInput):
    template_name = 'includes/clearable_file_input.html'
    initial_text = "Current Image"
    clear_checkbox_label = "Clear Image"
    input_text = "Choose New Image"

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        exclude = ['password',]

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        #we don't want the password on the form
        self.fields.pop('password')

        setFieldFormatting(self)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label='First Name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'First Name'}))
    last_name = forms.CharField(label='Last Name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        setFieldFormatting(self)


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('username', 'old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        setFieldFormatting(self)


def setFieldFormatting(target):
    attrs = {
        'placeholder' : ' ',
        'class' : 'form-control mb-1'
    }
    for field in target.fields:
        target.fields[field].widget.attrs.update(attrs)
    
    target.label_suffix = ''
    

# Update Contact Form
class UpdateContactForm(ModelForm):

    image = forms.ImageField(required=False, widget=CustomFileInput)
    
    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ('user',)
    def __init__(self, *args, **kwargs):
        super(UpdateContactForm, self).__init__(*args, **kwargs)
        setFieldFormatting(self)        

