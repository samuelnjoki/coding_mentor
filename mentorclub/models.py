from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from django.conf import settings
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email,username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        if not username:
            raise ValueError("The username field  must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username,password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username= models.CharField(max_length=30,unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phone=models.CharField(max_length=15)
    INTEREST=(
        ('','Your Interest?'),
        ('mentor','mentor'),
        ('mentee','mentee'),
    )
    interest=models.CharField(max_length=50,choices=INTEREST)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    image=models.ImageField(verbose_name='photo',blank=True,null=True,default='default.png')
    is_active = models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    

    # Add custom fields here

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
    
    def __str__(self):
        return self.username
    
    def has_perm(self,perm,obj=None):
        return self.is_admin 
       
    def has_module_perm(self,app_label):
        return True


class Course(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField(max_length=15000)
    price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    image=models.ImageField(default='default1.png')
    
    
    def __str__(self):
        return str(self.title)
    
class Member(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    EXPERIENCE=(
        ('','Experience Period'),
        ('None','None'),
        ('1-6 months','1-6 months'),
        ('6-12 months','6-12 months'),
        ('1-2 yrs','1-2 yrs'),
        ('2-4 yrs','2-4 yrs'),
        ('above 4yrs','above 4yrs'),
    )
    INTEREST=(
        ('','Your Interest?'),
        ('mentor','mentor'),
        ('mentee','mentee'),
        
    )
    experience=models.CharField(max_length=20,choices=EXPERIENCE)
    interest=models.CharField(max_length=50,choices=INTEREST)
    
    
    
    def __str__(self):
        return f'{self.user.username}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_user_course'),
        ]
        def __str__(self):
            return f"{self.user.username}"


class Event(models.Model):
    title=models.CharField(max_length=255)
    date=models.DateField()
    fromT=models.TimeField()
    toT=models.TimeField()
    description=models.TextField(max_length=15000)
    image=models.ImageField()
    
    def __str__(self):
        return self.title

class Schedule(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    mentor=models.ForeignKey(Member,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    description=models.TextField(max_length=15000)
    date=models.DateField()
    fromT=models.TimeField()
    toT=models.TimeField()
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'mentor'], name='unique_course_mentor'),
        ]
        def __str__(self):
            return f"{self.user.mentor}"