import mimetypes
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
# Create your models here.

class Tag(models.Model):
    tagname = models.CharField(max_length=50)
    emoji = models.CharField(max_length=5, blank=True)
    
    def __str__(self):
        return f"{self.emoji} {self.tagname}"
    
class Location(models.Model):
    location_name = models.CharField(max_length=100)

    def __str__(self):
        return self.location_name


from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin  
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Please enter a validate emaill address.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(email, password, **extra_fields)
        


def validate_image_or_video(file):
    # Get the MIME type of the file
    mime_type, _ = mimetypes.guess_type(file.name)
    if mime_type:
        if not mime_type.startswith('image') and not mime_type.startswith('video'):
            raise ValidationError("Only image or video files are allowed.")
    else:
        raise ValidationError("Could not determine file type.")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    birth_date = models.DateField()
    user_name = models.CharField(max_length=40 ,unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['birth_date']

    def __str__(self):
        return self.email
    

class ProfileMedia(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='profile_medias')

    def user_dir_path(instance, filename):
        return  f'👤{instance.user.user_name}/{filename}'

    media = models.FileField(upload_to=user_dir_path, validators=[validate_image_or_video])


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length = 120, blank = True)
    tags = models.ManyToManyField(Tag, blank = True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank = True,null = True)

    def __str__(self):
        return f"{self.user.user_name}'s Profile"





# user.profile_media.all()