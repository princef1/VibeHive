import mimetypes
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.models import Q
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

    def full_name(self):
        return self.first_name+ ' ' +self.last_name
    
    @property
    def friends(self):
    # Get all Friendships where this user is user1 or user2
        friendships = Friendship.objects.filter(Q(user1=self) | Q(user2=self))
        friend_ids = []
        for f in friendships:
            if f.user1 == self:
                friend_ids.append(f.user2.id)
            else:
                friend_ids.append(f.user1.id)
        return CustomUser.objects.filter(id__in=friend_ids)

    @property
    def friend_count(self):
        return self.friends.count()
        

    def __str__(self):
        return self.email
    

class ProfileMedia(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='media')

    def user_dir_path(instance, filename):
        return  f'👤{instance.user.user_name}/{filename}'

    media = models.FileField(upload_to=user_dir_path, validators=[validate_image_or_video])

    mime_type = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if self.media:
            mime, _ = mimetypes.guess_type(self.media.name)
            self.mime_type = mime or ''
        super().save(*args, **kwargs)

    @property
    def is_video(self):
        return self.mime_type.startswith('video/')

    @property
    def is_image(self):
        return self.mime_type.startswith('image/')


class UserProfile(models.Model):

    def user_profile_pic_path(instance, filename):
        return f"profile_pics/{instance.user.user_name}/{filename}"

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to=user_profile_pic_path, blank=True, null=True)
    bio = models.TextField(max_length = 120, blank = True)
    tags = models.ManyToManyField(Tag, blank = True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank = True,null = True)
    is_complete = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.user.user_name}'s Profile"


# Friendship
class FriendRequest(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_requests',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_requests',
        on_delete=models.CASCADE
    )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"


class Friendship(models.Model):
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='friendship_user1',
        on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='friendship_user2',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} ↔ {self.user2}"
    
def are_friends(user1, user2):
        return Friendship.objects.filter(
            models.Q(user1=user1, user2=user2) | models.Q(user1=user2, user2=user1)
        ).exists()
