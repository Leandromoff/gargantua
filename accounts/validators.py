import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ComplexPasswordValidator:
    """
    Validador de senha que exige:
    - Pelo menos 8 caracteres
    - Pelo menos uma letra minúscula
    - Pelo menos uma letra maiúscula
    - Pelo menos um número
    """
    
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("A senha deve ter pelo menos 8 caracteres."),
                code='password_too_short',
            )
        
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos uma letra minúscula."),
                code='password_no_lower',
            )
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos uma letra maiúscula."),
                code='password_no_upper',
            )
        
        if not re.search(r'\d', password):
            raise ValidationError(
                _("A senha deve conter pelo menos um número."),
                code='password_no_number',
            )
    
    def get_help_text(self):
        return _(
            "Sua senha deve conter pelo menos 8 caracteres, incluindo "
            "pelo menos uma letra minúscula, uma maiúscula e um número."
        )

