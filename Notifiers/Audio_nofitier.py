####### IMPORTING #######
import winsound


######## OTHER FUNCTIONS #########
def audio_beep(freq=320, duration=1000):
    winsound.Beep(freq, duration)