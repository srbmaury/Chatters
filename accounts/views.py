from django.core.mail import EmailMessage, send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import profile as profile_model
from .models import *
from .forms import RegisterForm
from .forms import ProfileUpdateForm
from .tokens import generate_token
from feed.models import post

def register(request):
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    username = request.POST.get('username')
    email = request.POST.get('email')
    if request.method == 'POST':  
        form = RegisterForm(request.POST)  
        if form.is_valid():
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = "Confirm your Email @ Chatters Login!!"
            message = render_to_string('email_confirmation.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':generate_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            messages.success(request, "Please confirm your email address to complete the registration")
            return render(request, 'accounts/login.html')  
        elif password1 != password2:
            messages.error(request, 'Passwords did not match')
            return redirect('register')
        elif User.objects.exclude(pk=form.instance.pk).filter(username=username).exists():
            messages.error(request, 'Username already taken. Please try another one')
            return redirect('register')
        elif User.objects.exclude(pk=form.instance.pk).filter(email=form.instance.email).exists():
            messages.error(request, 'Email already taken. Please try another one')
            return redirect('register')
        else:
            messages.error(request, 'Please choose a stronger password')
            return redirect('register')
    else:  
        form = RegisterForm()  
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
        except:
            user = None
        
        try:
            user2 = User.objects.get(email=email)
        except:
            user2 = None
        
        if user2 is not None:
            user = user2
        if user is not None:
            if user.profile.is_verified:
                if user.check_password(password):
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, "Incorrect password")
                    return redirect('/login')
            else:
                messages.error(request, "Your email is not verified. Check your email for verification")
                return redirect('/login')
        else:
            messages.error(request, 'Invalid username or Email')
            return redirect('/login')
    return render(request, 'accounts/login.html')

def activate(request,uidb64,token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        myuser.profile.email_token = token
        myuser.profile.is_verified = True
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        return render(request,'activation_failed.html')

@login_required
def profile(request):
    user = User.objects.get(username = request.user.username)
    posts_list = []
    for posts in post.objects.all():
        if posts.uname == user:
            posts_list.append(posts)
    posts_list.sort(key=lambda x: x.datetime, reverse=True)

    context = {
        'user': user,
        'posts_list': posts_list,
    }
    return render(request, 'accounts/profile.html', context)

def profileupdate(request):
    pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    image = request.FILES.get('image')
    bio = request.POST.get('bio')
    
    if(request.method == 'POST'):
        if pform.is_valid:
            pform.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        pform = ProfileUpdateForm(instance=request.user.profile)
        
    return render(request, 'accounts/profileupdate.html',{'pform':pform})

def change_password(request):
    if request.method == 'POST':
        user = request.user
        form = PasswordChangeForm(request.user, request.POST)
        old_password = request.POST.get('old_password')
        password = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('profile')
        elif user.check_password(old_password) == False:
            messages.error(request, 'Old password is incorrect')
            return redirect('change_password')
        elif password != password2:
            messages.error(request, 'New password and confirm password did not match')
            return redirect('change_password')
        else:
            messages.error(request, 'Please choose a stronger password')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/changepassword.html', {
        'form': form
    })

def show_profiles(request):
    user = User.objects.all()
    # user_profile = profile_model.objects.all()
    if request.user.is_superuser:
        return render(request, 'accounts/viewprofilelist.html',{'users':user})


