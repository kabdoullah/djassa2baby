from django.core.mail import EmailMessage
import threading


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
