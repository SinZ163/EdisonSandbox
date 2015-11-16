# coding=UTF8

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

import json
import time
import mraa
import requests

from I2cLCDRGBBackLit import I2CLCDDisplay
from TH02 import TH02
from music import Music

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=""
consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=""
access_token_secret=""

weather_api = "" #TODO: Config file

reply_tweet = "@{name} It is currently {temp} degrees, {fact} and {sunset:.2f} hours until sunset"

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def init(self):
        self.display.I2cLCDInit() #Clear the display completely
        self.display.LEDColor(0x55,0xAC,0xEE) #Twitter Blue
        #self.display.LCDInstruction(0x04) #Display on, Cursor OFF, blink OFF
    def __init__(self, api):
        self.api = api
        self.display = I2CLCDDisplay()
        self.music = Music()
        self.sensor = TH02(bus=1)
        self.uv = mraa.Aio(0)
        self.init()
    def on_data(self, data):
        data = json.loads(data)
        self.init()
        self.display.LCDPrint("@" + data["user"]["screen_name"][:15])
       
        print("@{screen_name} {text}".format(screen_name=data["user"]["screen_name"], text=data["text"]))
        displayText = data["text"]
        
        #This is to show the first word(s) well
        self.display.LCDInstruction(0x80+0x28) #Row 2, Column 0x00
        self.display.LCDPrint(displayText[:16])
        self.music.play()

        r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Hawthorn,Australia&appid=" + weather_api) 
        info = r.json()
        print(info)
    
        self.api.update_status(
                               status=reply_tweet.format(
                                    temp = self.sensor.getTemperature(),
                                    name = data["user"]["screen_name"],
                                    fact = 
info["weather"][0]["description"],
                                    sunset = (int(info["sys"]["sunset"]) - int(time.time())) / 60.0 / 60.0
                               ),
                               in_reply_to_status_id = data["id"])
        time.sleep(5)
        
        while(len(displayText) >= 16):
            self.display.LCDInstruction(0x80+0x28) #Row 2, Column 0x04
            self.display.LCDPrint(displayText[:16])
            time.sleep(0.5)
            displayText = displayText[1:]
        time.sleep(2)
        self.init()
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    api = API(auth)
    l = StdOutListener(api)
    stream = Stream(auth, l)
    stream.filter(track=['#swinburne'])
    
    #api = API(auth)
    #time.sleep(10)
    
    #sensor = TH02(bus=1)
    #api.update_status(status="It is currently {0}° Degrees in TC303 #Swinburne".format(sensor.getTemperature()))
