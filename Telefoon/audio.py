import time

import numpy as np
import pyaudio as pyaudio
from mutagen.mp3 import MP3
import vlc


base_folder = 'Telefoon/sounds'
min_peak = 300


def play(sound, wait):
    player = vlc.MediaPlayer(base_folder + "/" + sound + ".mp3")
    player.play()
    if wait:
        audio = MP3(base_folder + "/" + sound + ".mp3")
        time.sleep(audio.info.length)
    return player


def listen():
    while True:
        try:
            p = pyaudio.PyAudio()

            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=48000,
                            input_device_index=1,
                            input=True)

            for i in range(int(1000 * 48000 / 1024)):

                data = np.frombuffer(stream.read(512), dtype=np.int16)
                peak = np.average(np.abs(data)) * 2

                if peak > min_peak:
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    return True
            else:
                stream.stop_stream()
                stream.close()
                p.terminate()
        except OSError:
            pass
