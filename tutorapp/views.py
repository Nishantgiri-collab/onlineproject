from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegistrationUserForm, LoginForm,ClassBookingForm
from .models import RegistrationUser
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
from functools import wraps
# Create your views here.
from django.conf import settings
from django.core.mail import send_mail



def reg_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("reg_user_id"):
            messages.error(request, "⚠️ Please login first.")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper

def add_show(request):
    return render(request, 'registration.html')

def home(request):
    return render(request, 'home.html')



def register_user(request):
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Collect user info for WhatsApp
            user_info = f"""
            🎉 New Registration Successful on OnlineTutor.com 🎉

            Name: {user.fullname}
            Phone: {user.phone_number}
            Age: {user.age}
            Qualification: {user.previous_qualification}
            Percentage: {user.previous_qualification_percentage}
            Email: {user.email}
            """

            # Send WhatsApp message via Twilio
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                client.messages.create(
                    body=user_info,
                    from_=settings.TWILIO_WHATSAPP_NUMBER,
                    to=settings.MY_WHATSAPP_NUMBER
                )
            except Exception as e:
                print("WhatsApp Error:", e)
                # ✅ Gmail notification
                try:
                    send_mail(
                        subject="New Registration on OnlineTutor.com",
                        message=user_info,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[settings.EMAIL_HOST_USER],  # send to admin Gmail
                        fail_silently=False,
                    )
                except Exception as e:
                    print("Email Error:", e)
            messages.success(request, "✅ You have successfully registered on OnlineTutor.com!")
            return redirect('login')
    else:
        form = RegistrationUserForm()
    return render(request, 'registration.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = RegistrationUser.objects.get(email=email)
                if user.password == password:  # ❌ (still plain text)
                    request.session["reg_user_id"] = user.id   # ✅ save in session
                    messages.success(request, "Login successful!")
                    return redirect('book_class')
                else:
                    messages.error(request, "Invalid password.")
            except RegistrationUser.DoesNotExist:
                messages.error(request, "User does not exist.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


from django.shortcuts import get_object_or_404
from .models import ClassSlot
def book_class(request):
    reg_user_id = request.session.get("reg_user_id")   # ✅ safe access
    if not reg_user_id:
        messages.error(request, "⚠️ Please login first.")
        return redirect("login")

    # fetch RegistrationUser
    reg_user = get_object_or_404(RegistrationUser, id=reg_user_id)

    # Check if the user already booked a slot
    existing_booking = ClassSlot.objects.filter(user=reg_user).first()
    if existing_booking:
        messages.warning(request, "⚠️ You have already booked a slot. Only one booking is allowed.")
        return render(request, "booking.html", {"existing_booking": existing_booking})

    if request.method == "POST":
        form = ClassBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = reg_user
            booking.phone_number = reg_user.phone_number
            booking.save()
            messages.success(request, "✅ Slot booking has been done successfully! Our tutor will reach out to you shortly.")
            return redirect("book_class")
        else:
            messages.error(request, "⚠️ Please select a slot before booking.")
    else:
        form = ClassBookingForm()

    return render(request, "booking.html", {"form": form})