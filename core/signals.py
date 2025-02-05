from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.core.exceptions import ValidationError

@receiver(user_logged_in)
def restrict_email_domain(sender, request, user, **kwargs):
    allowed_domains = ['gmail.com']  # Replace with your domain(s)
    email_domain = user.email.split('@')[1]
    if email_domain not in allowed_domains:
        raise ValidationError(f"Unauthorized domain: {email_domain}")
