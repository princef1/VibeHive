from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from myApp import models
from myApp.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserSetupProfile
from django.db.models.signals import post_delete,pre_save
from django.dispatch import receiver
from myApp.models import CustomUser, FriendRequest, Friendship, ProfileMedia, UserProfile
from django.contrib import messages
from .models import are_friends
from django.db.models import Q
# Create your views here.

def landingpage(request):
    return render(request, 'landingpage.html')

def signup(request):
        if request.user.is_authenticated:
            return redirect('feed')


        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('setup_profile')
        else:
            form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})
        
def user_login(request):
        if request.user.is_authenticated:
            return redirect('feed')


        if request.method == 'POST':
            form = CustomAuthenticationForm(request, request.POST)
            if form.is_valid():
                email = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=email, password=password)
                
                if user is not None:
                    login(request, user)
                    if hasattr(user, 'profile') and not user.profile.is_complete:
                        return redirect('setup_profile')
                    else:
                        return redirect('feed')
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


# def feed(request):
#     seen_user_names = request.session.get('seen_user_names', [])
#     friends_ids = [f.id for f in get_friends(request.user)]

#     # Get users who are NOT the current user, NOT friends, and NOT already shown
#     users = CustomUser.objects.filter(
#         is_staff=False,
#         is_superuser=False
#     ).exclude(
#         id=request.user.id
#     ).exclude(
#         user_name__in=seen_user_names
#     ).exclude(
#         id__in=friends_ids
#     )

#     # Optional: exclude users who have a pending friend request from/to you
#     pending_ids = FriendRequest.objects.filter(
#         Q(sender=request.user) | Q(receiver=request.user),
#         status='pending'
#     ).values_list('sender_id', 'receiver_id', named=False)
#     flat_pending_ids = set([id for pair in pending_ids for id in pair if id != request.user.id])
#     users = users.exclude(id__in=flat_pending_ids)

#     return render(request, "feed.html", {"users": users})

def feed(request):
    user = request.user

    # Friends
    friends_ids = [f.id for f in get_friends(user)]

    # Pending or accepted requests
    requested_ids = FriendRequest.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).values_list('sender_id', 'receiver_id', flat=False)

    request_related_ids = set()
    for sender_id, receiver_id in requested_ids:
        request_related_ids.add(sender_id)
        request_related_ids.add(receiver_id)

    # Only include "real" users (exclude self, friends, requests, superusers, staff, empty usernames)
    users = CustomUser.objects.exclude(id=user.id) \
        .exclude(id__in=friends_ids) \
        .exclude(id__in=request_related_ids) \
        .exclude(is_superuser=True) \
        .exclude(is_staff=True) \
        .exclude(user_name__isnull=True) \
        .exclude(user_name__exact='')

    return render(request, "feed.html", {"users": users})



def next_user(request, user_name):
    seen_user_names = request.session.get('seen_user_names',[])
    if user_name not in seen_user_names:
        seen_user_names.append(user_name)
    request.session['seen_user_names'] = seen_user_names

    return redirect(feed)

def friendrequest(request):
    pending_requests = FriendRequest.objects.filter(
        receiver=request.user,
        status='pending'
    ).select_related('sender')  # Optimize queries
    return render(request, 'friendrequest.html', {'pending_requests': pending_requests})

def profile(request, user_name):
    user_obj = get_object_or_404(CustomUser, user_name=user_name)

    received_request_obj = FriendRequest.objects.filter(
    sender=user_obj,
    receiver=request.user,
    status='pending'
    ).first()
    
    # Check if the current logged-in user is friends with the profile user
    is_friend = are_friends(request.user, user_obj)

    # Friend request status
    sent_request = FriendRequest.objects.filter(
        sender=request.user,
        receiver=user_obj,
        status='pending'
    ).exists()

    received_request = FriendRequest.objects.filter(
        sender=user_obj,
        receiver=request.user,
        status='pending'
    ).exists()

    # Friend count and friend list
    friend_count = user_obj.friend_count  # total friends
    friend_list = user_obj.friends        # list of CustomUser objects

    return render(request, "profile.html", {
        "user": user_obj,
        "received_request_obj": received_request_obj,
        "is_friend": is_friend,
        "sent_request": sent_request,
        "received_request": received_request,
        "friend_count": friend_count,
        "friend_list": friend_list,
    })




def setup_profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    # Prevent access if profile already completed
    if profile.bio and profile.tags.exists() and profile.location and profile.user.media.exists():
        return redirect('feed')

    if request.method == 'POST':
        form = UserSetupProfile(request.POST, request.FILES, instance=profile)
        media_files = request.FILES.getlist('media')
        

        if form.is_valid():
            form.save()
                # To handle media upload (upto 6 files total)
            existing_count = profile.user.media.count()
            upload_count = min(6 - existing_count, len(media_files))

            for media in media_files[:upload_count]:
                ProfileMedia.objects.create(user=user, media=media)

            if (profile.bio and
            profile.tags.exists() and
            profile.location and 
            profile.user.media.exists()
            ):
                profile.is_complete = True
                profile.save()
                
            return redirect('feed')
    else:
        form = UserSetupProfile(instance=profile)
    return render(request, 'setup_profile.html', {'form':form})

def edit_profile(request):
    return render(request,'editprofile.html')





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

def search_user(request):
    query = request.GET.get('q')
    users = CustomUser.objects.filter(user_name__icontains=query)
    return render(request, 'search_results.html', {'users': users})

# Friends
def send_friend_request(request, user_name):
    if request.method == "POST":
        receiver = get_object_or_404(CustomUser, user_name=user_name)
        sender = request.user

        if sender == receiver:
            messages.error(request, "You cannot send a request to yourself.")
        else:
            friend_request, created = FriendRequest.objects.get_or_create(
                sender=sender, receiver=receiver
            )
            if created:
                messages.success(request, f"Friend request sent to {receiver.user_name}!")
            else:
                messages.warning(request, "You have already sent a request to this user.")

        redirect_to = request.POST.get("next", None)
        if redirect_to == "feed":
            return redirect("feed")
        elif redirect_to == "profile":
            return redirect("profile", user_name=receiver.user_name)
        else:
            return redirect("feed")




def respond_friend_request(request, request_id, action):
    fr = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    
    if action == 'accept':
        fr.status = 'accepted'
        fr.save()

        user1, user2 = sorted([fr.sender, fr.receiver], key=lambda u: u.id)
        Friendship.objects.get_or_create(user1=user1, user2=user2)

        messages.success(request, f"You are now friends with {fr.sender.user_name}!")
    elif action == 'reject':
        fr.status = 'rejected'
        fr.save()
        messages.info(request, "Friend request rejected.")

    return redirect('friend_requests')

def cancel_friend_request(request, user_name):
    receiver = get_object_or_404(CustomUser, user_name=user_name)
    FriendRequest.objects.filter(sender=request.user, receiver=receiver, status='pending').delete()
    messages.info(request, f"Friend request to {receiver.user_name} canceled ❌")
    return redirect('profile', user_name=user_name)


def unfriend(request, user_name):
    friend = get_object_or_404(CustomUser, user_name=user_name)

    # Delete friendship
    Friendship.objects.filter(
        Q(user1=request.user, user2=friend) |
        Q(user1=friend, user2=request.user)
    ).delete()

    # Clean up any friend requests (pending, accepted, rejected) between them
    FriendRequest.objects.filter(
        Q(sender=request.user, receiver=friend) |
        Q(sender=friend, receiver=request.user)
    ).delete()

    messages.info(request, f"You unfriended {friend.user_name}.")
    return redirect('profile', user_name=user_name)
    


def get_friends(user):
    friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
    friends = [f.user1 if f.user2 == user else f.user2 for f in friendships]
    return friends

def friend_list(request):
    user = request.user
    friends = get_friends(user)
    return render(request, 'friendlist.html', {'friends': friends})

def user_friend_list(request, user_name):
    user_obj = get_object_or_404(CustomUser, user_name=user_name)
    friends = get_friends(user_obj)
    return render(request, 'friend_list.html', {'friends': friends, 'user_obj': user_obj})

def chat(request):
    return render(request,'chat.html')



