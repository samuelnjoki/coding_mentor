
from mentorclub.models import Course, Event, User



def all(request):
    return{
        'allusers':User.objects.all().count(),
        'allcourses':Course.objects.all().count(),
        'allevents':Event.objects.all().count(),
        'allmentors':User.objects.filter(interest="mentor").count(),
        }