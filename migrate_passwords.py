import os
import sys
import django
from django.contrib.auth.hashers import make_password

# Setup Django Environment
sys.path.append(r"d:\Project MCA\house_new_testing\house")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "house.settings")
django.setup()

from house.models import Login, Register

print("Starting Heavy Encryption for Database...")

# Loop 1: Core Login Table
login_count = 0
for user in Login.objects.all():
    # Only encrypt if it is not already a safe hash
    if not user.password.startswith('pbkdf2_'):
        user.password = make_password(user.password)
        user.save()
        login_count += 1
print(f"Encrypted {login_count} plaintext passwords in the Login table.")

# Loop 2: Master Registration Table
reg_count = 0
for reg in Register.objects.all():
    if not reg.password.startswith('pbkdf2_'):
        reg.password = make_password(reg.password)
        reg.save()
        reg_count += 1
print(f"Encrypted {reg_count} plaintext passwords in the Register table.")

print("100 percent of Legacy Database Passwords are now Militarily Encrypted!")
