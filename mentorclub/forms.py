from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from mentorclub.models import Course, Member,User


 
class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("username","email","firstname","lastname","phone","bio","interest","gender","password1","password2",)
    
    
    
    def clean_username(self):
        username=self.cleaned_data['username']
        
        try:
            user=User.objects.get(username=username)
        
        except Exception as e:
            return username
        raise forms.ValidationError(f'Username {user.username} is already in use. ')
    
    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            user=User.objects.get(email=email)
        
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} is already in use. ')
    
    
class UserAddForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("username","email","firstname","lastname","phone","interest","is_admin","is_staff","is_superuser","password1","password2",)
    
    
    
    def clean_username(self):
        username=self.cleaned_data['username']
        
        try:
            user=User.objects.get(username=username)
        
        except Exception as e:
            return username
        raise forms.ValidationError(f'Username {user.username} is already in use. ')
    
    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            user=User.objects.get(email=email)
        
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} is already in use. ')
    
    

class AccountAuthenticationForm(forms.ModelForm):
    password=forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    
    class Meta:
        model = User
        fields=('username','password',)
    
    def clean(self):
        if self.is_valid():
            username=self.cleaned_data['username']
            password=self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid Credentials.")


class UserUpdateForm(forms.ModelForm):
    interest=forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder':'Your interest','readonly': 'readonly'})
        )
    email=forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={'placeholder':'email'})
        )
    username=forms.CharField(
        label='',
       
        widget=forms.TextInput(attrs={'placeholder':'username', 'autofocus':True,})
        )
    firstname=forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder':'First Name','readonly': 'readonly'})
        )
    lastname=forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder':'Last Name','readonly': 'readonly'})
        )
    image=forms.ImageField(
        label='',
        widget=forms.FileInput(attrs={'placeholder':'photo'})
        )
    # experience=forms.CharField(
    #     label='',
    #     widget=forms.TextInput(attrs={'placeholder':'Experience'})
    #     )
    phone=forms.CharField(
        label='',
        max_length=13,
        min_length=9,
        validators=[RegexValidator(
            r'^[0-9]*$',
            message='Invalid phone number!')],
        widget=forms.TextInput(attrs={'placeholder':'phone number'})
        )
    # course=forms.ModelChoiceField(
    #     queryset=Course.objects.all(),
    #     label='',
    #     widget=forms.Select(attrs={'placeholder':'Your interest'})
    #     )
    class Meta:
        model = User
        fields = ["firstname","lastname","username","gender","interest","email","phone","image"]
        

class UserEditForm(forms.ModelForm):
    
    # interest=forms.CharField(
    #     label='',
    # )
    # gender=forms.CharField(
    #     label='',
    #     widget=forms.TextInput(attrs={'placeholder':'Gender, male or female'})
    # )
    email=forms.EmailField(
        label='',
        widget=forms.TextInput(attrs={'placeholder':'email'})
        )
    username=forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder':'username','autofocus':True,})
        )
    firstname=forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder':'First Name',})
        )
    lastname=forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder':'Last'})
        )
    image=forms.ImageField(
        label='',
        widget=forms.FileInput(attrs={'placeholder':'Last'})
        )
    # experience=forms.CharField(
    #     label='',
    #     widget=forms.TextInput(attrs={'placeholder':'Experience'})
    #     )
    phone=forms.CharField(
        label='',
        max_length=13,
        min_length=9,
        validators=[RegexValidator(
            r'^[0-9]*$',
            message='Invalid phone number!')],
        widget=forms.TextInput(attrs={'placeholder':'phone number'})
        )
    # course=forms.ModelChoiceField(
    #     queryset=Course.objects.all(),
    #     label='',
    #     widget=forms.Select(attrs={'placeholder':'Your interest'})
    #     )
    class Meta:
        model = User
        fields = ["firstname","lastname","username","gender","interest","email","phone","image",'is_active','is_admin','is_staff']
        labels={
            'gender':'',
            'interest':'',
        }
        widget={
            'gender':forms.Select(attrs={'class':'form-control'}),
            'interest':forms.Select(attrs={'class':'form-control'}),
        }



class CourseEnrolForm(forms.ModelForm):
    
    INTEREST=[
        ('mentee','mentee'),
        ('mentor','mentor')
        ]
    interest=forms.CharField(
        label='Your Interest',
        widget=forms.RadioSelect(
            choices=INTEREST
        )
    )
    class Meta:
        model = Member
        fields = ['user','course','experience','interest']
        
    def __init__(self,user, *args, **kwargs):
        super(CourseEnrolForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['course'].widget = forms.HiddenInput()

class MpesaPaymentForm(forms.Form):
    phone_number=forms.CharField(max_length=13,label='Phone Number')
    amount=forms.DecimalField(max_digits=8,decimal_places=2,label='Amount')