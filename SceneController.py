from WitchGamePlay import *
import pygame
import os
import RPi.GPIO as GPIO

class SceneController:
    def __init__(self):
        GPIO.cleanup()
        self.__scenePlay = GamePlay()
      #  os.environ["SDL_VIDEODRIVER"] = "dummy"
       # pygame.init()
        #size = width, height = 1920, 1080
        #screen = pygame.display.set_mode(size)


    def begin(self):
        self.__scenePlay.FSM.changeState(Waiting())

        while 1:

          #  self.handleEvents(pygame.event.get())

            self.__scenePlay.update()

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                # self.serialConnection.close()
                self.endGame()
                exit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.endGame()
                        exit()

    def endGame(self):
        self.__gamePlay.FSM.changeState(Quit())
      #  pygame.quit()


SceneController().begin()
