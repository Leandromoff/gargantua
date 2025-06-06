import string
import secrets
from django.core.mail import send_mail
from django.conf import settings


def generate_random_password(length=12):
    """Gera uma senha aleatória segura"""
    # Garantir que a senha tenha pelo menos um de cada tipo de caractere
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    
    # Pelo menos um de cada tipo
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
    ]
    
    # Completar o resto da senha
    all_chars = lowercase + uppercase + digits
    for _ in range(length - 3):
        password.append(secrets.choice(all_chars))
    
    # Embaralhar a senha
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)


def send_password_email(email, username, password):
    """Envia email com a senha gerada para o usuário"""
    subject = 'Sua conta foi criada - Sistema Gargantua Users'
    message = f"""
Olá {username},

Sua conta foi criada no sistema Gargantua Users.

Dados de acesso:
- Usuário: {username}
- Senha: {password}

Por favor, faça login e altere sua senha assim que possível.

Atenciosamente,
Equipe Gargantua Users
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

