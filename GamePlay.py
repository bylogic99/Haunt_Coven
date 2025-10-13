from Input import Input
from StateMachine import StateMachine
from ParlorGameStates import *
from Trigger import Trigger
from InfoBeamerMessenger import InfoBeamerMessenger

class GamePlay:

    def __init__(self):

        self.ResetButton = Input(17,"Reset",self.__handleResetButton)
        self.StartButton = Input(24,"Start",self.__handleStartButton)
        self.Lights = Trigger(26)
        self.Spotlight = Trigger(20)

        self.FSM = StateMachine(self, Empty())
        self.FSM.setGlobalState(Global())

        self.MessageManager = InfoBeamerMessenger()

    def update(self):
        self.Lights.Tick()
        self.Spotlight.Tick()
        self.FSM.update()

    def __handleResetButton(self, channel):
        if channel == 17:            
            self.handleMessage("RESET")

    def __handleStartButton(self, channel):
        if channel == 24:            
            self.handleMessage("START")


    def handleMessage(self, msg):
        return self.FSM.handMessage(msg)