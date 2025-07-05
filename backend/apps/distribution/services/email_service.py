# backend/apps/distribution/services/email_service.py

def send_email(content):
    """
    Versende E-Mail mit deinem Mail-Service.
    """
    # Beispiel mit Django's send_mail:
    # from django.core.mail import send_mail
    # send_mail(subject=content.title, message=content.body, from_email=..., recipient_list=...)
    print(f"Sende E-Mail: '{content.title}' an Empfängerliste")
