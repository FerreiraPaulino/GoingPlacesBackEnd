from django.core.mail import send_mail

class Util():
    @staticmethod
    def send_mail(data):
        send_mail(data['email_subject'], data['email_message'], data['from'], [data['to']])