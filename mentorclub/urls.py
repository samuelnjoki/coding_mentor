
from django.urls import path


from mentorclub import views


urlpatterns = [
    path('', views.index,name='index'),
    path('admin-page/',views.admin_view,name='admin_page'),
    path('admin-page/users/',views.alluser,name='alluser'),
    path('admin-page/add-user/',views.registerUser,name='adduser'),
    path('admin-page/add-user/delete/<str:pk>/',views.delete,name='delete'),
    path('admin-page/course/',views.allcourse,name='allcourse'),
    path('admin-page/users/edituser/<str:pk>/',views.edituser,name='edituser'),
    path('contact/', views.contact,name='contact'),
    path('admin-page/users/user-info/<str:pk>/',views.userInfo,name='userinfo'),
    path('about/', views.about,name='about'),
    path('courses/', views.courses,name='courses'),
    path('events/', views.events,name='events'),
    path('mentors/', views.mentors,name='mentors'),
    path('coursementors/', views.courseMentors,name='course_mentors'),
    path('register/',views.register,name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('myprofile/',views.myprofile,name='myprofile'),
    path('myprofile/profile-update/',views.profile_update, name='proupdate'),
    path('course-details/<str:pk>/',views.course_details, name='course_details'),
    path('enrol/',views.enrol,name='enrol'),
    path('enrol/<str:pk>/',views.enrol,name='enrol'),
    path('mentoring/',views.mentoringCourses,name='coursesmentoring'),
    path('mentored/',views.mentoredCourses,name='mentoredcourses'),
    path('pay/',views.pay,name="pay"),
    path('token/',views.token,name="token"),
    path('stk/',views.stk,name='stk'),
    
]