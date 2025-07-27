from django.core.exceptions import ValidationError
import re

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError('A senha deve ter no mínimo 8 caracteres.')
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError('A senha deve conter pelo menos uma letra (a-z ou A-Z).')
        if not re.search(r'\d', password):
            raise ValidationError('A senha deve conter pelo menos um número (0-9).')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('A senha deve conter pelo menos um caractere especial (ex: !@#$%).')

    def get_help_text(self):
        return (
            "A senha deve ter no mínimo 8 caracteres, incluindo pelo menos uma letra, "
            "um número e um caractere especial."
        )
