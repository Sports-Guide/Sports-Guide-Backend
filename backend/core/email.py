from djoser import email


class CustomActivationEmail(email.ActivationEmail):
    """
    Отправка письма для подтверждения почты.
    """
    template_name = 'core/email/activation.html'


class CustomPasswordResetEmail(email.PasswordResetEmail):
    """
    Отправка письма восстановления пароля.
    """
    template_name = 'core/email/password_reset.html'
