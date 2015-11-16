#Import time from the core python library
import time
#Mess with a button
import mraa

NOTE_B0 = 31
NOTE_C1 = 33
NOTE_CS1 = 35
NOTE_D1 = 37
NOTE_DS1 = 39
NOTE_E1 = 41
NOTE_F1 = 44
NOTE_FS1 = 46
NOTE_G1 = 49
NOTE_GS1 = 52
NOTE_A1 = 55
NOTE_AS1 = 58
NOTE_B1 = 62
NOTE_C2 = 65
NOTE_CS2 = 69
NOTE_D2 = 73
NOTE_DS2 = 78
NOTE_E2 = 82
NOTE_F2 = 87
NOTE_FS2 = 93
NOTE_G2 = 98
NOTE_GS2 = 104
NOTE_A2 = 110
NOTE_AS2 = 117
NOTE_B2 = 123
NOTE_C3 = 131
NOTE_CS3 = 139
NOTE_D3 = 147
NOTE_DS3 = 156
NOTE_E3 = 165
NOTE_F3 = 175
NOTE_FS3 = 185
NOTE_G3 = 196
NOTE_GS3 = 208
NOTE_A3 = 220
NOTE_AS3 = 233
NOTE_B3 = 247
NOTE_C4 = 262
NOTE_CS4 = 277
NOTE_D4 = 294
NOTE_DS4 = 311
NOTE_E4 = 330
NOTE_F4 = 349
NOTE_FS4 = 370
NOTE_G4 = 392
NOTE_GS4 = 415
NOTE_A4 = 440
NOTE_AS4 = 466
NOTE_B4 = 494
NOTE_C5 = 523
NOTE_CS5 = 554
NOTE_D5 = 587
NOTE_DS5 = 622
NOTE_E5 = 659
NOTE_F5 = 698
NOTE_FS5 = 740
NOTE_G5 = 784
NOTE_GS5 = 831
NOTE_A5 = 880
NOTE_AS5 = 932
NOTE_B5 = 988
NOTE_C6 = 1047
NOTE_CS6 = 1109
NOTE_D6 = 1175
NOTE_DS6 = 1245
NOTE_E6 = 1319
NOTE_F6 = 1397
NOTE_FS6 = 1480
NOTE_G6 = 1568
NOTE_GS6 = 1661
NOTE_A6 = 1760
NOTE_AS6 = 1865
NOTE_B6 = 1976
NOTE_C7 = 2093
NOTE_CS7 = 2217
NOTE_D7 = 2349
NOTE_DS7 = 2489
NOTE_E7 = 2637
NOTE_F7 = 2794
NOTE_FS7 = 2960
NOTE_G7 = 3136
NOTE_GS7 = 3322
NOTE_A7 = 3520
NOTE_AS7 = 3729
NOTE_B7 = 3951
NOTE_C8 = 4186
NOTE_CS8 = 4435
NOTE_D8 = 4699
NOTE_DS8 = 4978

melody = [
  NOTE_C7, NOTE_G7, NOTE_C7, NOTE_G7, NOTE_C7, NOTE_G7, NOTE_C7, NOTE_G7
]
#Mario main them tempo
tempo = [
  20, 20,20, 20,20, 20,20, 20
]
class Music():
    def __init__(self):
        self.led = mraa.Gpio(13)
        self.led.dir(mraa.DIR_OUT)
        self.buzzer = mraa.Gpio(4)
        self.buzzer.dir(mraa.DIR_OUT)
    def buzz(self, frequency, length):
        self.led.write(1)
        for i in xrange((frequency * length)/1000):
                self.buzzer.write(1)
                #0.000001 is microseconds
                time.sleep(1.0 / frequency / 2)
                self.buzzer.write(0)
                time.sleep(1.0 / frequency / 2)
        self.led.write(0)
    def play(self):
        for i in xrange(len(melody)):
            if melody[i] != 0:
                print(str(1.0 / melody[i] / 2) + " | " + str(tempo[i]))
            else:
                print("0 | "+str(tempo[i]))
            self.buzz(melody[i], 1000/tempo[i])
            time.sleep(1 / (tempo[i] * 1.3))
            #buzz(0, 1000/tempo[i])
            
if __name__ == "__main__":
    music = Music()
    music.play()
