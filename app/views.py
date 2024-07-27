from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm   # default form by django
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm #created by me
from .middlewares import auth, guest  # import middlewares
# email imports
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User



# Create your views here.


@guest
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
            # return redirect('dashboard')
    else:
        initial_data = {'username':'', 'first_name':'', 'email':'', 'last_name':'', 'password1':'', 'password2':''}

        form = CustomUserCreationForm(initial = initial_data)

    return render(request, 'app/register.html', {'form':form})

@guest
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
            
    else:
        initial_data = {'username':'', 'password':''}

        form = AuthenticationForm(initial = initial_data)

    return render(request, 'app/login.html', {'form':form})

@auth
def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')



# #creating a new register_view 
# @guest
# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # Deactivate account till it is confirmed
#             user.save()
#             send_verification_email(request, user)
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'app/register.html', {'form': form})

# def send_verification_email(request, user):
#     current_site = get_current_site(request)
#     mail_subject = 'Activate your account.'
#     message = render_to_string('app/activation_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': default_token_generator.make_token(user),
#     })
#     to_email = user.email
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     email.send()

# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return redirect('dashboard')
#     else:
#         return render(request, 'app/activation_invalid.html')