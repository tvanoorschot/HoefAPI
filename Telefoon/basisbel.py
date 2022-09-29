import time
from datetime import datetime

from API import apns
from API.gebruiker.gebruiker_repository import get_all_gebruikers
from API.oproep.oproep_repository import *
from Telefoon import telefoon, cam, audio


def start():
    try:
        wait_seconds = 60

        # if audio.listen():
        if True:
            print("Aangebeld")

            for gebruiker in get_all_gebruikers():
                if gebruiker.token is not None:
                    apns.send_oproep_notification(gebruiker)

            telefoon.openemen()

            audio.play("welkom", True)

            date_now = datetime.now().strftime('%Y-%m-%d %H:%M')
            # picture_url = cam.take_picture(date_now)

            oproep = save_oproep(Oproep(time=date_now, picture=""))
            oproep_id = oproep.id

            player = audio.play("wachtmuziek", False)

            while True:
                oproep = select_oproep(oproep_id)
                if wait_seconds == 0 and oproep.opnemer is None:
                    oproep_opnemen(id=oproep_id, opnemer_id=1)
                    oproep_reageren(id=oproep_id, reactie="Geen reactie ontvangen")
                    print("Geen reactie ontvangen")

                    for gebruiker in get_all_gebruikers():
                        if gebruiker.token is not None:
                            apns.clear_notifications(gebruiker)

                    player.stop()
                    audio.play("geen_reactie", True)
                    telefoon.ophangen()
                    break
                else:
                    if wait_seconds == 15 or wait_seconds == 30 or wait_seconds == 45 or wait_seconds == 60:
                        print(wait_seconds)

                    if oproep.reactie is not None:
                        player.stop()
                        if oproep.reactie == "Ik kom er aan":
                            audio.play("kom_er_aan", True)
                            telefoon.ophangen()
                        break
                    time.sleep(1)
                    wait_seconds -= 1
    except TimeoutError:
        telefoon.ophangen()
