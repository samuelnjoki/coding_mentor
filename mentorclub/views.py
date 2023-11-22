from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages

from mentorclub.forms import AccountAuthenticationForm, CourseEnrolForm, RegistrationForm, UserAddForm, UserEditForm, UserUpdateForm
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout

from mentorclub.models import Course, Event, Member, Schedule, User

from requests.auth import HTTPBasicAuth
import json
import requests
# from mentorclub.credentials import LipanaMpesaPpassword,MpesaAccessToken

# Create your views here.

def admin_view(request):
    return render(request,'admin.html')

def alluser(request):
    users=User.objects.all()
    return render(request,'alluser.html',{'users':users})

def allcourse(request):
    courses=Course.objects.all()
    return render(request,'allcourses.html',{'courses':courses})


# @user_passes_test(lambda user: user.groups.filter(name='admin').exists(),login_url='login')
def edituser(request,pk):
    user=User.objects.get(id=pk)
    form = UserEditForm(instance=user)
    if request.method == 'POST':
        form = UserEditForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'User Profile  updated  successfully ')
            return redirect('userinfo',pk=user.id)
            

    context = {
        'form': form,
        'user':user,
       
    }
    return render(request, 'edituser.html', context)

def userInfo(request,pk):
    user=User.objects.get(id=pk)
    return render(request,'Userprofile.html',{'user':user})

def index(request):
    mentee=User.objects.filter(interest="mentee").count()
    mentor=User.objects.filter(interest="mentor").count()
    event=Event.objects.all().count()
    course=Course.objects.all().count()
    context={
        'mentee':mentee,
        'mentor':mentor,
        'course':course,
        'event':event,
    }
    return render(request,'index.html',context)

def about(request):
    mentee=Member.objects.filter(interest="mentee").count()
    mentor=Member.objects.filter(interest="mentor").count()
    event=Event.objects.all().count()
    course=Course.objects.all().count()
    context={
        'mentee':mentee,
        'mentor':mentor,
        'course':course,
        'event':event,
    }
    return render(request,'about.html',context)

def contact(request):
    return render(request,'contact.html')


def courses(request):
    # available_courses = Member.objects.filter(interest="mentor").values('course')
    # course = Course.objects.filter(id__in=available_courses)
    course=Course.objects.all()
    return render(request,'courses.html',{'course':course})

def mentors(request):
    mentor=Member.objects.filter(interest="mentor")
    context={
        'mentor':mentor
    }
    return render(request,'mentors.html',context)
def courseMentors(request):
    mentor=User.objects.filter(interest="mentor")
    context={
        'mentor':mentor
    }
    return render(request,'coursementors.html',context)
def events(request):
    event=Event.objects.all()
    return render(request,'events.html',{'event':event})

@login_required(login_url='login')
def course_details(request,pk):
    
    try:
        course=Course.objects.get(id=pk)
        schedule=Schedule.objects.filter(course=course.id).last()
        mentee=Member.objects.filter(course=course.id,interest="mentee").count()
        
        context={
            'course':course,
            'mentee':mentee,
            'schedule':schedule
            }
        return render(request,'course-details.html',context)
    except:
        course=Course.objects.get(id=pk)
        mentee=Member.objects.filter(course=course.id,interest="mentee").count()
        
        context={
            'course':course,
            'mentee':mentee,
            }
        return render(request,'course-details.html',context)
    
def registerUser(request):
    course=Course.objects.all()
    context={
        'course':course
    }
    if request.POST:
        form=UserAddForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request,'User Account Created successfully ')
            username=form.cleaned_data.get('username')
            raw_pass=form.cleaned_data.get('password1')
            account=authenticate(username=username,password=raw_pass)
            if account is not None:
                messages.success(request,'User Account Created successfully ')
                return redirect("adduser")
            else:
                return redirect('adduser')
        else:
            context['user_add_form']=form
    return render(request,'adduser.html',context)


def register(request):
    course=Course.objects.all()
    context={
        'course':course
    }
    if request.POST:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Created successfully ')
            username=form.cleaned_data.get('username')
            raw_pass=form.cleaned_data.get('password1')
            account=authenticate(username=username,password=raw_pass)
            if account is not None:
                # login(request, account)
                return redirect("login")
            else:
                return redirect('/')
        else:
            context['registration_form']=form
    return render(request,'register.html',context)

def login_view(request):
    user=request.user
    if user.is_authenticated:
        return redirect('index')
    context={
        
    }
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return redirect('login')
        else:
            context['login_form']=form
    return render(request,'login.html',context)

def logout_view(request):
    logout(request)
    return redirect('index')

def myprofile(request):
    user=request.user
    return render(request,'myprofile.html')

  
@login_required(login_url='login')
def profile_update(request):

    if request.method == 'POST':
        form = UserUpdateForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile  updated  successfully ')
            return redirect('myprofile')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
        
    }
    return render(request, 'profile_update.html', context)

def enrol(request,pk):
    course=Course.objects.get(id=pk)
    
    if request.method=='POST':
        form=form=CourseEnrolForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'You have successfully enrolled for {course.title} ')
            return redirect('courses')
        else:
            messages.error(request, f'already enrolled for {course.title}')
            return render(request,'enrol.html',{'form':form,'course':course})
    else:
        form=form=CourseEnrolForm(request.user,initial={'course':course.id})
        context={
            'form':form,
            'course':course
        }
        return render(request,'enrol.html',context)
def mentoringCourses(request):
     # Retrieve courses related to the current user
    user_courses = Member.objects.filter(user=request.user,interest="mentor").values('course')

    # Get the actual Course objects based on the filtered course IDs
    course = Course.objects.filter(id__in=user_courses)
    
    return render(request,'mentorcourses.html',{'course':course})

def mentoredCourses(request):
     # Retrieve courses related to the current user
    user_courses = Member.objects.filter(user=request.user,interest="mentee").values('course')

    # Get the actual Course objects based on the filtered course IDs
    course = Course.objects.filter(id__in=user_courses)
    
    return render(request,'menteecourses.html',{'course':course})


def delete(request, pk):
    product = User.objects.get(id=pk)
    product.delete()
    return redirect('alluser')




# payement functions


def token(request):
    pass
    # consumer_key = 'UUFquEZIk5XryNGVfMeEL0JefkCZ7DkX'
    # consumer_secret = 'cH4LDrAgE6AV8Wg7'
    # api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    # r = requests.get(api_URL, auth=HTTPBasicAuth(
    #     consumer_key, consumer_secret))
    # mpesa_access_token = json.loads(r.text)
    # validated_mpesa_access_token = mpesa_access_token["access_token"]

    # return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
    return render(request, 'pay.html')

def stk(request):
    pass
    # if request.method =="POST":
    #     phone = request.POST['phone']
    #     amount = request.POST['amount']
    #     access_token = MpesaAccessToken.validated_mpesa_access_token
    #     # api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    #     headers = {"Authorization": "Bearer %s" % access_token}
    #     request = {
    #         "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
    #         "Password": LipanaMpesaPpassword.decode_password,
    #         "Timestamp": LipanaMpesaPpassword.lipa_time,
    #         "TransactionType": "CustomerPayBillOnline",
    #         "Amount": amount,
    #         "PartyA": phone,
    #         "PartyB": LipanaMpesaPpassword.Business_short_code,
    #         "PhoneNumber": phone,
    #         "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
    #         "AccountReference": "Apen Softwares",
    #         "TransactionDesc": "Web Development Charges"
    #     }
    #     response = requests.post(api_url, json=request, headers=headers)
    #     result=response.json()
    #     if 'errorCode' in result:
    #         error_message = result.get('errorMessage', 'Unknown error')
    #         return HttpResponse(f'<h1>Payment initiation failed: {error_message}</h1>')

    # # Check for specific scenarios where the transaction may fail
    #     if result.get('ResponseCode') == '0':
    #         if result.get('ResultCode') == '1032':
    #             return HttpResponse('<h1>Payment initiation successful, but customer did not complete the transaction. Please try again.</h1>')
    #         elif result.get('ResultCode') == '2001':
    #             return HttpResponse('<h1>Payment initiation successful, but customer has insufficient funds. Please ensure you have enough money in your account.</h1>')
    #         else:
    #             return HttpResponse('<h1>Payment initiation successful!</h1>')
    #     else:
    #         return HttpResponse('<h1>Payment initiation failed. Please check your account balance and try again.</h1>')