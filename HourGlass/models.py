from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch  import receiver
from django.http import Http404
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image')
    bio = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()  

    class Meta:
        db_table = 'profile'

    @receiver(post_save, sender=User)
    def update_create_profile(sender,instance,created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


    def save_profile(self):
        self.save()

class Diary(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    author_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default='1', blank = True)

    def save_diary(self):
        self.save()
    def __str__(self):
        return f'{self.author} Post'
    class Meta:
        db_table = 'diary'
        ordering = ['-created_date']
    def delete_diary(self):
        self.delete()
    @classmethod
    def search_diary(cls,search_term):
        diary = cls.objects.filter(title__icontains=search_term)
        return diary

    @classmethod
    def get_diary(cls,id):
        try:
            diary = Diary.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise Http404()
        return Diary