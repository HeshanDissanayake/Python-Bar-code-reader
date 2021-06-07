from picamera.array import PiRGBArray
from picamera import PiCamera
import pyzbar.pyzbar as pyz
import vlc
import time

#

audio = {   b'Tba.' : "Tuba.mp3",
            b'Tbn.' : "Trombone.mp3",
            b'A. Sax.' :"Alto Saxophone.mp3",
            b'B. Cl.' : "Bass Clarinet.mp3",
            b'Euph.' : "Euphonium.mp3",
            b'B\xe7\xac\x99\xef\xbd\xad Cl.': "B Clarinet.mp3",
            b'Fl.' : "Flute.mp3",
            b'T. Sax.' : "Tenor Saxophone.mp3",
            b'F Hn.' : "Horn in F.mp3",
            b'B\xe7\xac\x99\xef\xbd\xad Tpt.':"B Trumpet.mp3"}

class AudioTrack():
    '''class for handling media player'''
    def __init__(self, audiopath):
        self.mp = vlc.MediaPlayer("audio/%s"%audiopath)
        self.isplaying = False
        self.t1 = 0

    def play(self):
        self.t1 = time.time()
        self.isplaying = True
        self.mp.play()

    def stop(self):
        if (time.time() - self.t1) < 3:
            return
        self.isplaying = False
        self.mp.stop()
    def updateTimer(self):
        self.t1 = time.time()

if __name__ == '__main__':

    # initialize the Pi camera
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    tracks = {}

    # build a Audiotrack instace for all tracks in the 'audio' dictionary
    for audio_ in audio.values():
        track = AudioTrack(audio_)
        tracks[audio_] = track

    # read images from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array

        # decode QRcodes
        QRcodes = pyz.decode(img)

        toPlayTracks = list()

        for QRcode in QRcodes:
            print(audio[QRcode.data])
            if audio[QRcode.data] in audio.values():
                toPlayTracks.append(audio[QRcode.data])
            else:
                print("Unkown QR code")

        if len(toPlayTracks) != 0:
            print('QRcode detected')

        for toPlayTrack in toPlayTracks:
            tracks[toPlayTrack].updateTimer()
            if not tracks[toPlayTrack].isplaying:
                tracks[toPlayTrack].play()
                print('playing ', toPlayTracks)

        for track in tracks.keys():
            if track not in toPlayTracks:
                tracks[track].stop()
