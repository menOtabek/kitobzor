import requests
from django.conf import settings


def send_telegram_message_code(data, request):
    message = (
        f"📞 Telefon: {data.phone or 'Ko‘rsatilmagan'}\n"
        f"👤 Ism: {request.user.first_name}\n"
        f"👤 Familiya: {request.user.last_name}\n"
        f"📞 Telegram: {request.user.phone_number}\n\n"
        f"💬 Xabar: {data.message}\n"

    )

    url = 'https://api.telegram.org/bot{token}/sendMessage?text={message}&chat_id={chat_id}'.format(
        token=settings.MESSAGE_BOT_TOKEN,
        message=requests.utils.quote(message),
        chat_id=settings.MESSAGE_CHANNEL_ID
    )

    requests.get(url)
