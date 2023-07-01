from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.generic import View

#TO GET TOKEN FROM utils.py
from .utils import TokenGenerator, generate_token

#TO ACTIVATE ACCOUNT
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

#TO SEND EMAIL
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.core.mail import BadHeaderError, send_mail
from django.core import mail
from django.conf import settings

#TO RESET PASSWORD
from django.contrib.auth.tokens import PasswordResetTokenGenerator

#THREADING
import threading

class  EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()



class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active=True
            user.save()
            messages.info(request, "Account Activated Sucessfully")

            return redirect('signin')
        return render(request, 'auth/activatefailed.html')
    


class RequestResetEmailView(View):
    def get(self, request):
        return (render(request, 'auth/reset_passwd.html'))
    
    def post(self, request):
        email = request.POST['e-mail']
        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = 'Reset Your Password'
            message = render_to_string('auth/reset_user_passwd.html', {
                'domain' : '127.0.0.1:8000',
                'uid' : urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token' : PasswordResetTokenGenerator().make_token(user[0])
            })

            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
            EmailThread(email_message).start()

            messages.info(request, "Please Check your Email for a link to reset your Password")
            return (render(request, 'auth/reset_passwd.html'))
        


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64' : uidb64,
            'token' : token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, "Password Reset Link is Invalid")
                return render(request, 'auth/reset_passwd.html')

        except DjangoUnicodeDecodeError as identifier:
            pass    

        return render(request, 'auth/set-new-passwd.html', context)
    
    def post(self, request, uidb64, token):
        context = {
            'uidb64' : uidb64,
            'token' : token
        }

        password = request.POST['passwd1']
        confirm_password = request.POST['passwd2']

        if password != confirm_password:
            messages.warning(request, "Passwords do not Match")
            return render(request, 'auth/set-new-passwd.html')
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password Reset Successful! Please Login with New Password")
            return redirect('signin')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "Something Went Wrong")
            return render(request, 'auth/set-new-passwd.html')



def signup(request):
    if request.method=="POST":
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['passwd1']
        confirm_password = request.POST['passwd2']

        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return render(request, 'auth/signup.html')
            
        try:
            if User.objects.get(username=email):


                messages.warning(request, "Email is already registered")
                return render(request, 'auth/signup.html')

        except Exception as identifier:
            pass
        
        user = User.objects.create_user(email, email, password)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)

        email_subject = "Activate Your Account"
        message = render_to_string('auth/activate.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email],)

        EmailThread(email_message).start()
        messages.info(request,"Please check your email for a link to activate your account")
        return redirect('signin')
    return render(request, 'auth/signup.html')


def signin(request):
    if request.method=="POST":

        username = request.POST['e-mail']
        userpassword = request.POST['passwd']
        myuser=authenticate(username = username, password = userpassword)

        if myuser is not None:
            login(request, myuser)
            messages.success(request,"Login Successful!")
            return render(request,'index.html')
        else:
            print(f"Authentication error: {myuser}")
            messages.error(request,"Invalid Credentials!")
            return redirect('signin')
    return render(request, 'auth/login.html')


def signout(request):
    logout(request)
    messages.success(request,"Logout Successful!")
    return redirect('signin')