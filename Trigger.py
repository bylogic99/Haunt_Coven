import RPi.GPIO as GPIO
import time
import numpy as np
from datetime import datetime

class Trigger:
    def __init__(self, Pin, Name):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Pin, GPIO.LOW, initial=0)
        self.__channel = Pin
        self.__isFiring = False
        self.__fireTime = 0
        self.__fireIntervals = []
        self.__fireIndex = 0
        self.__name = Name
        print("initialize output " + format(Pin))

    def __timesUp(self, prev_time, interval):
        if int(round(time.time() * 1000)) - prev_time > interval:
            prev_time = int(round(time.time() * 1000))
            return  True, prev_time
        else:
            return  False, prev_time

    def Fire(self, intervals):
        self.__isFiring=True
        self.__fireIndex = 0
        self.__fireIntervals = intervals
        self.__fireTime = int(round(time.time() * 1000))  # sets current time in millis

    def Reset(self):
        self.__isFiring = False
        GPIO.output(self.__channel, 0)

    def Tick(self):
        state = 0
        if self.__isFiring:
            if (self.__fireIndex % 2) == 0:  #even is on
                state = 1
            timesUp, self.__fireTime = self.__timesUp(self.__fireTime, self.__fireIntervals[self.__fireIndex])
            if not timesUp: # activate or continue to activate channel
               # print(self.__name + " is fireing ",self.__fireIndex,"  ",  self.__fireIntervals[self.__fireIndex], " ", state)
                GPIO.output(self.__channel, state)
            else: #move to next index or stop firing
                if self.__fireIntervals.__len__()-1 == self.__fireIndex: #end of firing sequence
                  #  print(self.__name + " is fireing false")
                    self.__isFiring = False
                    #GPIO.output(self.__channel, 0)
                else:
                 #   print(self.__name + " next fire index",self.__fireIndex + 1)
                    self.__fireIndex = self.__fireIndex + 1

    def isFiring(self):
        return self.__isFiring