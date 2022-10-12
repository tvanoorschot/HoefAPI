from uuid import uuid4

from aioapns import APNs, NotificationRequest, PushType

import settings
from API.gebruiker.gebruiker_repository import get_all_gebruikers


async def send_oproep_notification():
    for gebruiker in get_all_gebruikers():
        if gebruiker.token is not None:
            await send_notification({
                "aps": {
                    "alert": {
                        "title": "DING DONG!!",
                        "body": "Er heeft iemand aangebeld"
                    },
                    "interruption-level": "critical",
                    "badge": 1,
                    "sound": "bel.caf"
                }
            }, gebruiker)


async def send_second_oproep_notification():
    for gebruiker in get_all_gebruikers():
        if gebruiker.token is not None:
            await send_notification({
                "aps": {
                    "alert": {
                        "title": "DING DONG!!",
                        "body": "Nog 30 seconden om te reageren"
                    },
                    "interruption-level": "critical",
                    "badge": 1,
                    "sound": "bel.caf"
                }
            }, gebruiker)


async def clear_notifications():
    for gebruiker in get_all_gebruikers():
        if gebruiker.token is not None:
            await send_notification({
                "aps": {
                    "content-available": 1,
                    "badge": 0,
                    "priority": 10
                }
            }, gebruiker)


async def send_notification(message, gebruiker):
    if settings.development:
        apns_client = APNs(client_cert='resources/certs/pushcertdev.pem', use_sandbox=False)
    else:
        apns_client = APNs(client_cert='resources/certs/pushcert.pem', use_sandbox=False)

    request = NotificationRequest(
        device_token=gebruiker.token,
        message=message,
        notification_id=str(uuid4()),  # optional
        time_to_live=3,  # optional
        push_type=PushType.ALERT
    )
    await apns_client.send_notification(request)
