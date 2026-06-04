import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User
from django.contrib.auth.hashers import make_password

def reset_password(username, new_password):
    print(f"Reseteando contraseña para usuario: {username}")
    try:
        user = User.objects.get(username=username)
        user.password = make_password(new_password)
        user.is_active = True
        user.reset_failed_attempts()  # Limpia intentos y desbloquea
        user.save()
        print(f"Contraseña actualizada con éxito para {username}.")
    except User.DoesNotExist:
        print(f"Error: El usuario {username} no existe.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python scripts/reset_student_pass.py <usuario> <nueva_contraseña>")
        sys.exit(1)
    reset_password(sys.argv[1], sys.argv[2])
