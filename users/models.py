from django.db import models, IntegrityError
from django.contrib.auth.models import User, Group, Permission
from PIL import Image
from PIL import Image, UnidentifiedImageError
from django.db import models
from django.conf import settings
import os
from users.choices import CITY_CHOICES, ACTIVITIES_CHOICES, LEVEL_CHOICES
from locations.models import City


class Activity(models.Model):
    name = models.CharField(max_length=100, choices=ACTIVITIES_CHOICES)

    def __str__(self):
        return self.name

class ProfileActivity(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    skill_level = models.CharField(max_length=50,choices=LEVEL_CHOICES,blank=True,null=True)


    class Meta:
        unique_together = ('profile', 'activity')  # Ensures unique activity per profile
        
    def __str__(self):
        return f"{self.profile.user.username} - {self.activity.name} - {self.skill_level}"
    
# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')
    bio = models.TextField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=15, blank=True)
    hide_email = models.BooleanField(default=False)
    hide_telephone = models.BooleanField(default=False)
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_set", blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
            
            img = Image.open(self.avatar.path)

            if img.height > 100 or img.width > 100:
                new_img_size = (100, 100)
                img.thumbnail(new_img_size, Image.ANTIALIAS)
                img.save(self.avatar.path)

        except UnidentifiedImageError:
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'default.jpg')
            img = Image.open(default_image_path)
            img.save(self.avatar.path)
        
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            raise

        except Exception as e:
            print(f"Error saving profile image: {e}")



