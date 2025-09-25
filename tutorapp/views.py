from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegistrationUserForm, LoginForm,ClassBookingForm
from .models import RegistrationUser
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
# Create your views here.
def add_show(request):
    return render(request, 'registration.html')

def home(request):
    return render(request, 'home.html')

# Your Twilio credentials (get them from Twilio Console)
TWILIO_ACCOUNT_SID = "AC789c3e12c51836ae4ee062e8a2ff3f5b"
TWILIO_AUTH_TOKEN = "741111839d16ceed9edf4ee454538b47"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio Sandbox WhatsApp number
MY_WHATSAPP_NUMBER = "whatsapp:+919179167128"  # Your personal WhatsApp number


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
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                client.messages.create(
                    body=user_info,
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=MY_WHATSAPP_NUMBER
                )
            except Exception as e:
                print("WhatsApp Error:", e)

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
                if user.password == password:  # ❌ Not secure, better to hash passwords
                    messages.success(request, "Login successful!")
                    return redirect('book_class')
                else:
                    messages.error(request, "Invalid password.")
            except RegistrationUser.DoesNotExist:
                messages.error(request, "User does not exist.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from .models import ClassSlot
@login_required
def book_class(request):
    # Check if the user already booked a slot
    existing_booking = ClassSlot.objects.filter(user=request.user).first()
    if existing_booking:
        messages.warning(request, "⚠️ You have already booked a slot. Only one booking is allowed.")
        return render(request, "booking.html", {"existing_booking": existing_booking})
    if request.method == "POST":
        form = ClassBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "✅ Slot booking has been done successfully! Our tutor will reach out to you shortly.")
            return redirect('book_class')
        else:
            messages.error(request, "⚠️ Please select a slot before booking.")
    else:
        form = ClassBookingForm()

    return render(request, "booking.html", {"form": form})