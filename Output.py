import sys
import os
import threading
import time

import RPi.GPIO as GPIO


class Output:
    def __init__(self, pin, active_high=True):
        self.pin = pin
        self.active_high = active_high
        self.is_active = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        
        # Initialize to inactive state
        self._set_inactive()

    def activate(self):
        if self.active_high:
            GPIO.output(self.pin, GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.LOW)
        self.is_active = True

    def deactivate(self):
        self._set_inactive()

    def _set_inactive(self):
        if self.active_high:
            GPIO.output(self.pin, GPIO.LOW)
        else:
            GPIO.output(self.pin, GPIO.HIGH)
        self.is_active = False

    def is_activated(self):
        return self.is_active

    def toggle(self):
        if self.is_active:
            self.deactivate()
        else:
            self.activate()

    def get_state(self):
        return "Active" if self.is_active else "Inactive"

    def get_pin(self):
        return self.pin

    def cleanup(self):
        GPIO.cleanup(self.pin)

    @staticmethod
    def cleanup_all():
        GPIO.cleanup()