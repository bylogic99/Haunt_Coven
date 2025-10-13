import time

class Timer:

    def __init__(self, seconds):
        self.__gameSeconds = seconds
        self.__startTicks = 0
        self.__secondsRemaining = self.__gameSeconds
        self.__isRunning = 0

    def start(self):
        self.__isRunning = 1
        self.__gameSeconds = self.__secondsRemaining

    def reset(self):
        self.__secondsRemaining = self.__gameSeconds
        self.__isRunning = 0

    def tick(self):
        if self.__isRunning:
            self.__secondsRemaining = round(self.__gameSeconds - ((pygame.time.get_ticks() - self.__startTicks) / 1000))

    def getTime(self):
        return time.strftime("%M:%S", time.gmtime(self.__secondsRemaining))

    def isZero(self):
        return round(self.__gameSeconds - ((pygame.time.get_ticks() - self.__startTicks) / 1000)) <= 0

    def getTimeInSeconds(self):
        return round(self.__gameSeconds - ((pygame.time.get_ticks() - self.__startTicks) / 1000))