from django.apps import AppConfig


class MentorclubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mentorclub'
    
    def ready(self):
       import mentorclub.signals
