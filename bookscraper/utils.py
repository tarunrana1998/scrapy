# utils.py
from scrapy.mail import MailSender

def send_email(settings, subject, body, to):
    """Send an email using Scrapy's MailSender."""
    mailer = MailSender(
        smtphost=settings.get('MAIL_HOST'),
        mailfrom=settings.get('MAIL_FROM'),
        smtpuser=settings.get('MAIL_USER'),
        smtppass=settings.get('MAIL_PASS'),
        smtpport=settings.getint('MAIL_PORT'),
        smtptls=settings.getbool('MAIL_TLS'),
        smtpssl=settings.getbool('MAIL_SSL')
    )
    mailer.send(to=to, subject=subject, body=body)
    print("Email sent successfully!")
