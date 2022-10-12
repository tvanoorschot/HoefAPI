
import sounddevice  # niet verwijderen, anders werkt niks meer
import asyncio
import threading
import time
from datetime import datetime
from API import apns
from API.oproep.oproep_repository import *
from Telefoon import telefoon, cam, audio


class PlayWelkomSound(threading.Thread):

    def run(self, *args, **kwargs):
        audio.play(sound="welkom", wait=True)


class SendNotifications(threading.Thread):

    def run(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(apns.send_oproep_notification())
        time.sleep(1)
        loop.close()


class SendSecondNotifications(threading.Thread):

    def run(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(apns.send_second_oproep_notification())
        time.sleep(1)
        loop.close()


async def start():
    try:
        wait_seconds = 60

        if audio.listen():
            print("Aangebeld")
            play_welkom_sound = PlayWelkomSound()
            send_notification_task = SendNotifications()

            telefoon.openemen()
            play_welkom_sound.start()
            send_notification_task.start()

            date_now = datetime.now().strftime('%Y-%m-%d %H:%M')
            picture_url = cam.take_picture(date_now)
            oproep = save_oproep(Oproep(time=date_now, picture=picture_url))

            play_welkom_sound.join()
            send_notification_task.join()
            oproep_id = oproep.id

            player = audio.play(sound="wachtmuziek", wait=False)

            while True:
                oproep = select_oproep(oproep_id)
                if wait_seconds == 0 and oproep.opnemer is None:
                    oproep_opnemen(id=oproep_id, opnemer_id=1)
                    oproep_reageren(id=oproep_id, reactie="Geen reactie ontvangen")
                    print("Geen reactie ontvangen")
                    player.stop()
                    audio.play(sound="geen_reactie", wait=True)
                    telefoon.ophangen()
                    await apns.clear_notifications()
                    break
                else:
                    if wait_seconds == 30:
                        send_second_notification_task = SendSecondNotifications()
                        send_second_notification_task.start()

                    if oproep.reactie is not None:
                        player.stop()
                        if oproep.reactie == "Ik kom er aan":
                            audio.play(sound="kom_er_aan", wait=True)
                        if oproep.reactie == "Ik ben er":
                            audio.play(sound="ben_er", wait=True)
                        if oproep.reactie == "Ik kom er niet aan":
                            audio.play(sound="kom_er_niet_aan", wait=True)
                        telefoon.ophangen()
                        await apns.clear_notifications()
                        break
                    time.sleep(1)
                    wait_seconds -= 1
    except TimeoutError:
        telefoon.ophangen()
