import sounddevice  # niet verwijderen, anders werkt niks meer
import threading
import time

import settings
from API import apns
from API.oproep.oproep_repository import *
from Telefoon import telefoon

if not settings.development:
    from Telefoon import audio


class PlayWelkomSound(threading.Thread):

    def run(self, *args, **kwargs):
        audio.play(sound="welkom", wait=True)


async def start():
    try:
        wait_seconds = 60

        if audio.listen():
            print("Aangebeld")
            play_welkom_sound = PlayWelkomSound()

            telefoon.openemen()
            play_welkom_sound.start()

            oproep = create_oproep()

            await apns.send_oproep_notifications()

            play_welkom_sound.join()

            player = audio.play(sound="wachtmuziek", wait=False)

            while True:
                oproep = select_oproep(oproep.id)
                if wait_seconds == 0 and oproep.opnemer is None:
                    oproep_opnemen(id=oproep.id, opnemer_id=1)
                    oproep_reageren(id=oproep.id, reactie="Geen reactie ontvangen")
                    print("Geen reactie ontvangen")
                    player.stop()
                    audio.play(sound="geen_reactie", wait=True)
                    telefoon.ophangen()
                    await apns.send_clear_notifications()
                    break
                else:
                    if wait_seconds == 30:
                        await apns.send_second_oproep_notifications()

                    if oproep.reactie is not None:
                        player.stop()
                        if oproep.reactie == "Ik kom er aan":
                            audio.play(sound="kom_er_aan", wait=True)
                        if oproep.reactie == "Ik ben er":
                            audio.play(sound="ben_er", wait=True)
                        if oproep.reactie == "Ik kom er niet aan":
                            audio.play(sound="kom_er_niet_aan", wait=True)
                        telefoon.ophangen()
                        await apns.send_clear_notifications()
                        break
                    time.sleep(1)
                    wait_seconds -= 1
    except TimeoutError:
        telefoon.ophangen()
