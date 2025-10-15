from Input import Input
from StateMachine import StateMachine
from WitchSceneGameStates import *
from Trigger import Trigger
from InfoBeamerMessenger import InfoBeamerMessenger
from DMXController import DMXController, DMXTrigger

FOG_CHANNEL = 1
FOG_ON_VALUE = 255
FOG_OFF_VALUE = 0


class GamePlay:

    def __init__(self):

        self.ResetButton = Input(17, "Reset", self.__handleResetButton)
        self.StartButton = Input(24, "Start", self.__handleStartButton)

        self.Lights = Trigger(26, "Lights")

        self.DMXController = DMXController()
        self.FogMachine = DMXTrigger(
            self.DMXController,
            FOG_CHANNEL,
            "FogMachine",
            on_value=FOG_ON_VALUE,
            off_value=FOG_OFF_VALUE,
        )

        self.FSM = StateMachine(self, Empty())
        self.FSM.setGlobalState(Global())

        self.MessageManager = InfoBeamerMessenger()

    def update(self):
        self.Lights.Tick()
        #self.Spotlight.Tick()
        self.FogMachine.Tick()
        self.FSM.update()

    def __handleResetButton(self, channel):
        if channel == 17:
            self.handleMessage("RESET")

    def __handleStartButton(self, channel):
        if channel == 24:
            self.handleMessage("START")

    def handleMessage(self, msg):
        return self.FSM.handleMessage(msg)

