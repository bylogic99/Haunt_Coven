import RPi.GPIO as GPIO
import threading

class Input:
    def __init__(self, pin, name, callback):
        GPIO.setmode(GPIO.BCM)
        #GPIO.setup(Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.add_event_detect(Pin, GPIO.RISING, callback=self.button_callback, bouncetime=350)
        self.__pressed = False
        self.__enabled = False
        self.__channel = pin
        self.__callback = callback
        self.__name = name

        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        cb = ButtonHandler(pin, self.button_callback, edge='rising', bouncetime=50)
        cb.start()
        GPIO.add_event_detect(pin, GPIO.RISING, callback=cb)
        
        print("initialize button " + format(pin))

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
            self.__callback(channel)
            print(format(channel) + " pressed")
            self.__pressed = True

class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge='both', bouncetime=50):
        super().__init__(daemon=True)

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.func(*args)
            print("pinval" + str(pinval))

        self.lastpinval = pinval
        self.lock.release()