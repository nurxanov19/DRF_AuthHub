# Foydalanuvchi uchun bitta page ochiladi va tel yoki email so'raydi. Foydalanuvchi xohishiga qarab
# tel yoki email kiritadi va sms shu manzilga boradi (tel va emailni ajratish uchun RegEx dan foydalaniladi)

from django.core.mail import send_mail
import sms
from django.http import HttpResponse

from config import settings


class ConsoleSMSBackend:
    def send_sms(self, phone_number, message):
        print(f"Sending SMS to {phone_number}: {message}")


def sent_to_email(request, address, message):
    message = f"Hello! {address} \n\n{message}"
    subject = 'Confirmation code'
    address = address
    send_mail(subject, message, settings.EMAIL_HOST_USER, [address])


def send_sms_to_user(request):
    sms_backend = ConsoleSMSBackend()
    sms_backend.send_sms('+998901234567', 'Hello, this is a test SMS from Django!')
    return HttpResponse("SMS sent (check console)!")






