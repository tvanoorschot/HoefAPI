from uuid import uuid4
from aioapns import APNs, NotificationRequest, PushType

from API.gebruiker.gebruiker import Gebruiker


async def send_oproep_notification(gebruiker: Gebruiker):
    apns_client = APNs(client_cert='resources/certs/pushcertdev.pem', use_sandbox=True)

    request = NotificationRequest(
        device_token=gebruiker.token,
        message={
            "aps": {
                "alert": {
                    "title": "DING DONG!!",
                    "body": "Er heeft iemand aangebeld"
                },
                "interruption-level": "critical",
                "thread-id": "1",
                "sound": "bel.caf"
            }
        },
        notification_id=str(uuid4()),  # optional
        time_to_live=3,  # optional
        push_type=PushType.ALERT
    )
    await apns_client.send_notification(request)


async def clear_notifications(gebruiker: Gebruiker):
    apns_client = APNs(client_cert='resources/certs/pushcertdev.pem', use_sandbox=True)

    request = NotificationRequest(
        device_token=gebruiker.token,
        message={
            "aps": {
                "content-available": 1,
                "badge": 0,
                "priority": 10
            }
        },
        notification_id=str(uuid4()),  # optional
        time_to_live=3,  # optional
        push_type=PushType.ALERT
    )
    await apns_client.send_notification(request)
