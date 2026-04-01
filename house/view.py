from django.http import HttpResponse
from django.shortcuts import render,redirect;
from house import models
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.cache import never_cache
import re
from django.core.mail import send_mail
from django.conf import settings
import random

def home(request):
    property_list = models.AddProperty.objects.order_by('?')[:6]
    broker_list = models.Broker.objects.filter(profile_image__isnull=False).exclude(profile_image='').order_by('?')[:3]
    return render(request,'home/index.html', {'properties': property_list, 'brokers': broker_list}) 

def login(request):
    return render(request,'login/login.html')

# def save_data(request):
#     name = request.POST['name']
#     email = request.POST['email']
#     phone = request.POST['phone']
#     gender = request.POST['gender']
#     course = request.POST['course']
#     age = request.POST['age']
#     sdata = models.Students(name=name,email=email,phone=phone,gender=gender,course=course,age=age)
#     sdata.save()
#     return redirect('display_data')

def check_login(request):
    uname = request.POST['uname']
    password = request.POST['password']
    # Empty validation
    if not uname or not password:
        messages.error(request, "All fields are required")
        return redirect('login')
    
    # Password length validation
    if len(password) < 6:
        messages.error(request, "Password must be at least 6 characters")
        return redirect('login')

    udata = models.Login.objects.filter(user_name=uname).first()

    if udata:
        if check_password(password, udata.password):
            request.session['semail'] = udata.user_name
            request.session['seuser_id'] = udata.user_id
            if udata.user_type == 'admin':
                return redirect('../administrator/dashboardAdmin')
            elif udata.user_type == 'broker':
                return redirect('../broker/dashboardBroker')
            elif udata.user_type == 'user':
                return redirect('../user/userDashboard')
        else:
             messages.error(request, "Incorrect password!")
    else:
            messages.error(request, "Email not registered!")
    return redirect('login')

def register(request):
    return render(request,'home/register.html')

def register_user(request):
    if request.method == "POST":
        fname = request.POST['fullname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        address = request.POST['address']
        location = request.POST['location']
        user = "user"

        # Empty validation
        if not all([fname, email, phone, password, address, location]):
            messages.error(request, "All fields are required.")
            return redirect('register')
        
         # Name validation
        if not re.match(r"^[A-Za-z ]+$", fname):
            messages.error(request, "Invalid name format.")
            return redirect('register')
        
        # Email already exists
        if models.Register.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')
        
        # Password validation
        if len(password) < 8:
            messages.error(request, "Password too short.")
            return redirect('register')
        
        # Phone validation
        if not re.match(r"^[6-9][0-9]{9}$", phone):
            messages.error(request, "Invalid phone number.")
            return redirect('register')

        # Phone already exists
        if models.Register.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone already registered!")
            return redirect('register')

        # Save user
        hashed_password = make_password(password)
        Rdata = models.Register(
            full_name=fname,
            email=email,
            phone_number=phone,
            password=hashed_password,
            user_type=user,
            address=address,
            location=location
        )

        ldata = models.Login(
            user_name=email,
            password=hashed_password,
            user_type=user,
            status="active"
        )

        Rdata.save()
        ldata.save()

        messages.success(request, "Registration successful.")
        return redirect('login')

    return redirect('register')

def forgot_password(request):
    return render(request,'login/forgot_password.html')

def sendOtp(request):
    if request.method == "POST":
        email = request.POST.get("email")

        # Check email exists
        if not models.Register.objects.filter(email=email).exists():
            messages.error(request, "Email not registered.")
            return redirect("forgot_password")

        otp = random.randint(100000, 999999)

        # Save in session
        request.session["reset_email"] = email
        request.session["reset_otp"] = str(otp)

        # Send email
        send_mail(
            "Password Reset OTP",
            f"Your OTP is {otp}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        messages.success(request, "OTP sent to email.")
        return redirect("verify_otp")

    return redirect("forgot_password")

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        saved_otp = request.session.get("reset_otp")

        if entered_otp == saved_otp:
            messages.success(request, "OTP verified.")
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP.")
            return redirect("verify_otp")

    return render(request, "login/verify_otp.html")

def reset_password(request):
    return render(request,"login/reset_password.html")

def changeLoginPassword(request):
    # Ensure user came via OTP verification
    email = request.session.get("reset_email")
    if not email:
        messages.error(request, "Unauthorized access to password reset.")
        return redirect("login")

    if request.method == "POST":
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        # Validate password
        if not new_password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect("reset_password")

        if len(new_password) < 8:
            messages.error(request, "Password too short. Minimum 8 characters.")
            return redirect("reset_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")
        
        user = models.Register.objects.get(email=email)
        userl = models.Login.objects.get(user_name=email)
        hashed_password = make_password(new_password)
        user.password = hashed_password
        userl.password = hashed_password
        user.save()
        userl.save()
    return redirect("login")

def contact_view(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        models.Contact.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, "Your message has been sent!")

        # return HttpResponse("Message Sent Successfully!")

    return redirect('home')

    

@never_cache
def logout(request):
    request.session.flush()
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    return response




