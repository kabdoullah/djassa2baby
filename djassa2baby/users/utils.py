from django.core.mail import EmailMessage
import threading
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class EmailThread(threading.Thread):
    """Classe représentant un thread pour envoyer des e-mails de manière asynchrone"""

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        # Exécute la méthode send() de l'objet EmailMessage dans un thread séparé
        self.email.send()


class Util:

    """Classe utilitaire pour envoyer des e-mails de manière asynchrone"""

    @staticmethod
    def send_email(data):
        # Crée un objet EmailMessage avec les données fournies
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )

        # Crée un thread EmailThread avec l'objet EmailMessage et le démarre
        EmailThread(email).start()


def send_otp_email(shop, otp_code):

    """
        Envoie un email avec le code OTP au magasin (shop).
    """

    subject = "Votre code OTP pour vérifier votre compte"
    
    email_template = 'emails/send_otp.html'
    
    # Rendu du template avec les données contextuelles
    html_message = render_to_string(email_template, {'otp_code': otp_code, 'shop': shop, 'name': shop.name})
    plain_message = strip_tags(html_message)  # Email en texte brut (si l'email HTML n'est pas supporté)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [shop.email]  # Assure-toi que `Shop` a un champ email
    
    # Envoie de l'email
    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)



