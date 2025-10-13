import RPi.GPIO as GPIO

class Button:
    def __init__(self, Pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        GPIO.add_event_detect(Pin, GPIO.RISING, callback=self.button_callback, bouncetime=350)
        self.__pressed = False
        self.__enabled = False
        self.__channel = Pin
        print("initialize button " + format(Pin))

    def Enable(self):
        self.__enabled = True

    def Disable(self):
        self.__enabled = False

    def Pressed(self):
        if self.__pressed:
            self.__pressed = False
            return True
        return False

    def button_callback(self, channel):
        if self.__enabled and channel == self.__channel:
            print(format(channel) + " pressed")
            self.__pressed = True
