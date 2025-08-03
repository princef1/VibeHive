from django.shortcuts import redirect, render
from myApp.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from myApp.models import ProfileMedia
# Create your views here.

def landingpage(request):
    return render(request, 'landingpage.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
    
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('firstpage')
            else:
                print("Authentication Failed!!")
        else:
            print("Form invalid:", form.errors)
    else:
        form = CustomAuthenticationForm()
         
    return render(request, 'login.html', {'form':form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def firstpage(request):
    return render(request,'firstpage.html')

from django.db.models.signals import post_delete,pre_save
from django.dispatch import receiver


# To premanently delete the media from database (django saves it by default even when the admin deletes the media)
@receiver(post_delete, sender=ProfileMedia)
def delete_file_on_model_delete(sender, instance, **kwargs):
    if instance.media:
        instance.media.delete(save=False) 


# To replace the media deleting the replaced one from database (django saves the old media by default even when the admin replace the media)
@receiver(pre_save, sender=ProfileMedia)
def delete_old_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # It's a new object, no old file to delete

    try:
        old_file = sender.objects.get(pk=instance.pk).media
    except sender.DoesNotExist:
        return  # File does not exist yet

    new_file = instance.media
    if old_file and old_file != new_file:
        old_file.delete(save=False)

