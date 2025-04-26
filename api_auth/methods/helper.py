# Foydalanuvchi uchun bitta page ochiladi va tel yoki email so'raydi. Foydalanuvchi xohishiga qarab
# tel yoki email kiritadi va sms shu manzilga boradi (tel va emailni ajratish uchun RegEx dan foydalaniladi)

from django.core.mail import send_mail
from config import settings


def sent_to_email(request, address, message):
    message = f"Hello! {address} \n\n{message}"
    subject = 'Confirmation code'
    address = address
    send_mail(subject, message, settings.EMAIL_HOST_USER, [address])







