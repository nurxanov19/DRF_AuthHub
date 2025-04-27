# Foydalanuvchi uchun bitta page ochiladi va tel yoki email so'raydi. Foydalanuvchi xohishiga qarab
# tel yoki email kiritadi va sms shu manzilga boradi (tel va emailni ajratish uchun RegEx dan foydalaniladi)

from django.core.mail import send_mail
import sms
from django.http import HttpResponse
import logging
from config import settings
import threading

logging.basicConfig(level=logging.INFO)


class ConsoleSMSBackend:
    def send_sms(self, phone_number, message):
        print(f"Sending SMS to {phone_number}: {message}")


def sent_to_email(request, address, message):
    try:
        message = f"Hello! {address} \n\n{message}"
        subject = 'Confirmation code'
        address = address
        send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
        logging.info('Email sent successfully')
    except Exception as e:
        logging.exception(f'Failed to send email: {str(e)}')


def send_sms_to_user(request, phone_num):
    try:
        sms_backend = ConsoleSMSBackend()
        sms_backend.send_sms(phone_num, 'Hello, this is a test SMS from Django!')
        logging.info('SMS sent successfully! ')
        return HttpResponse("SMS sent (check console)!")
    except Exception as e:
        logging.exception(f'Failed to send sms: {str(e)}')

def run_thread(func, *args, **kwargs):
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()







