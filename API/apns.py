import collections

from apns2.client import APNsClient
from apns2.payload import Payload, PayloadAlert

import settings
from API.gebruiker.gebruiker_repository import get_all_gebruikers_with_token

topic = 'com.basishoef.deurbel'
Notification = collections.namedtuple('Notification', ['token', 'payload'])


async def send_clear_notifications():
    payload = Payload(
        badge=0,
        custom={"priority": "10", "content-available": "1"})

    send_notifications(payload, get_all_gebruikers_with_token())


async def send_second_oproep_notifications():
    payload = Payload(
        alert=PayloadAlert(title="DING DONG!!", body="Nog 30 seconden om te reageren"),
        sound="bel.caf",
        badge=1,
        custom={"interruption-level": "critical"})

    send_notifications(payload, get_all_gebruikers_with_token())


async def send_oproep_notifications():
    payload = Payload(
        alert=PayloadAlert(title="DING DONG!!", body="Er heeft iemand aangebeld"),
        sound="bel.caf",
        badge=1,
        custom={"interruption-level": "critical"})

    send_notifications(payload, get_all_gebruikers_with_token())


def send_notifications(payload, gebruikers):
    if settings.development:
        client = APNsClient('resources/certs/pushcertdev.pem', use_sandbox=True, use_alternative_port=False)
    else:
        client = APNsClient('resources/certs/pushcert.pem', use_sandbox=False, use_alternative_port=False)

    notifications = []
    for gebruiker in gebruikers:
        notifications.append(Notification(payload=payload, token=gebruiker.token))

    client.send_notification_batch(notifications=notifications, topic=topic)
