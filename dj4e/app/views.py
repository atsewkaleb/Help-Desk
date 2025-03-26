from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.shortcuts import render, get_object_or_404, redirect
from .models import Request
from .forms import ReqeustEditClient, ReqeustEditStaff, RequestEditForm, RequestForm
from .forms import UserRegistrationForm
from .tokens import account_activation_token
from django.contrib.auth.forms import AuthenticationForm




#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#Register -------------------------------------------------------------------------------------------------------------------------

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")
    return redirect('request_list')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': request.get_host(),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="registration/register_email.html",
        context={"form": form}
        )
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# log in and log out----------------------------------------------------------------------------------------------

def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")

def custom_login(request):
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect_based_on_role(user, request)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = AuthenticationForm()

    return render(
        request,
        template_name="registration/login.html",
        context={"form": form}
    )

def redirect_based_on_role(user, request):
    if user.role == 'ict_director':
        messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in as <b>ICT Director</b>")
        return redirect('request_list')
    elif user.role == 'team_leader':
        messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in as <b>Team Leader</b>")
        return redirect('request_list')
    elif user.role == 'staff':
        messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in as <b>Staff</b>")
        return redirect('request_list')
    elif user.role == 'client':
        messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in as <b>Client</b>")
        return redirect('request_list')
    else:
        logout(request)
        messages.error(request, "You are not authorized to access the website")
        return redirect('/')
    
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
# def register_email(request):
#     if request.method == 'POST':
#         form = EmailOnlyForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             if is_email_valid(email):
#                 user = create_user_from_csv(email, request)
#                 if user:
#                     return HttpResponse('Please check your email to complete registration.', status=200)
#                 else:
#                     return HttpResponse('User could not be created from CSV data.', status=400)
#             else:
#                 return HttpResponse('Email is not valid or not found in the CSV file.', status=400)
#     else:
#         form = EmailOnlyForm()
#     return render(request, 'registration/register_email.html', {'form': form})

#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

# request creation













@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.requester_email = request.user.email
            request_instance.requester_name = request.user.first_name
            request_instance.request_location = request.user.location
            request_instance.request_department = request.user.department
            request_instance.requester_phone = request.user.phone
            request_instance = form.save()
            return redirect('view_request', pk=request_instance.pk)
    else:
        form = RequestForm()
    return render(request, 'requests/create_request.html', {'form': form})

@login_required
def view_request(request, pk):
    request_instance = get_object_or_404(Request, pk=pk)
    return render(request, 'requests/view_request.html', {'request_instance': request_instance})

@login_required
def request_list(request):
    user = request.user
    if user.role == 'team_leader':
        requests = Request.objects.filter(assigned_team_leader=user)
    elif user.role == 'staff':
        requests = Request.objects.filter(assigned_staff=user)
    elif user.role == 'client':
        requests = Request.objects.filter(requester_email=user.email)
    elif user.role == 'ict_director':
        requests = Request.objects.all()
    else:
        requests = Request.objects.none()
        
    return render(request, 'requests/request_list.html', {'requests': requests})

@login_required
def edit_request(request, pk):
    user = request.user
    request_instance = get_object_or_404(Request, pk=pk)
    if request.method == 'POST':
        if user.role == 'client':
            form = ReqeustEditClient(request.POST, instance=request_instance)
        elif user.role == 'staff':
            form = ReqeustEditStaff(request.POST, instance=request_instance)
        else :
            form = RequestEditForm(request.POST, instance=request_instance)
        if form.is_valid():
            form.save()
            return redirect('view_request', pk=request_instance.pk)
    else:
        if user.role == 'client':
            form = ReqeustEditClient(instance=request_instance)
        elif user.role == 'staff':
            form = ReqeustEditStaff(instance=request_instance)
        else :
            form = RequestEditForm(instance=request_instance)
    return render(request, 'requests/edit_request.html', {'form': form, 'request_instance': request_instance})
