
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
# Create your models here.
PHONE_VALIDATOR = RegexValidator(
    r'^\+?\d{10,15}$', 'Enter a valid phone number (10–15 digits).'
)

class RegistrationUser(models.Model):
    fullname = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=15, validators=[PHONE_VALIDATOR])
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(100)]
    )
    previous_qualification = models.CharField(max_length=50)
    previous_qualification_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    email = models.EmailField(unique=True, max_length=50)
    password = models.CharField(max_length=15)
    confirm_password = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname


class ClassSlot(models.Model):
    SLOT_CHOICES = [
        ("Class 5-8 (Mon-Fri 4:00-5:00pm)", "Class 5 to 8 - All Subjects (Mon-Fri 4:00pm - 5:00pm)"),
        ("Class 9-10 (Mon-Fri 6:00-7:00pm)", "Class 9 & 10 - Science & Maths (Mon-Fri 6:00pm - 7:00pm)"),
        ("Class 11-12 (Mon-Fri 7:30-8:30pm)", "Class 11 & 12 - PCM (Mon-Fri 7:30pm - 8:30pm)"),
        ("Special Class 5-8 (Sat-Sun 11:00-12:00pm)", "Special Class 5 to 8 - All Subjects (Sat-Sun 11:00am - 12:00pm)"),
        ("Special Class 9-10 (Sat-Sun 4:00-5:00pm)", "Special Class 9 & 10 - Science & Maths (Sat-Sun 4:00pm - 5:00pm)"),
        ("Special Class 11-12 (Sat-Sun 5:30-6:00pm)", "Special Class 11 & 12 - PCM (Sat-Sun 5:30pm - 6:00pm)"),
    ]

    user = models.ForeignKey(RegistrationUser, to_field="email", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, validators=[PHONE_VALIDATOR])
    slot = models.CharField(max_length=100, choices=SLOT_CHOICES)
    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.fullname} ({self.user.email}) booked {self.slot}"
