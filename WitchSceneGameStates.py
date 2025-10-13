##---------------------------------------------------

class Global(object):

        def Name(cls):
            return "GLOBAL"

        def Enter(cls,owner):
            print("enter Global")


        def Execute(cls, owner):
            owner.Lights.Tick()
            message = owner.MessageManager.getData()
            if message == "finished\n":
               # print(message)
                owner.FSM.changeState(QuickScare())



        def Exit(cls, owner):
            print("Exiting Global")
            #owner.ResetButton.Deactivate()

        def OnMessage(cls,owner):
            return False
##---------------------------------------------------

class Empty(object):

        def Name(cls):
            #cls.Database.SetGameStatus(0, cls.gameClock.getTimeInSeconds(),0)  # Offline
            return "EMPTY"

        def Enter(cls,owner):
            print("enter Empty")

        def Execute(cls, owner):
            x=1

          #  print("Executing Empty")

        def Exit(cls, owner):
            print("Exiting Empty")

        def OnMessage(cls,owner):
            return False


##---------------------------------------------------

class Waiting(object):

        def Name(cls):
            return "WAITING"

        def Enter(cls,owner):
            print("enter waiting")
            owner.ResetButton.Enable()
            owner.StartButton.Enable()
            owner.FogMachine.Reset()
            owner.Lights.Reset()

            owner.MessageManager.sendWaiting()

        def Execute(cls, owner):
            if owner.StartButton.Pressed():
                owner.FSM.changeState(Intro())
            if owner.ResetButton.Pressed():
                owner.FSM.changeState(QuickScare())

        def Exit(cls, owner):
            print("Exiting waiting")
            owner.ResetButton.Disable()
            owner.StartButton.Disable()

        def OnMessage(cls,owner):
            return False

##---------------------------------------------------

class Intro(object):

        __prevClockTime = 0

        def Name(cls):
            return "INTRO"

        def Enter(cls,owner):
            print("enter Intro")
            owner.StartButton.Enable()
            owner.ResetButton.Enable()
            owner.MessageManager.sendIntro()
            owner.Lights.Fire([0,15000,20,300,20,300,10,200,20,500,10,100,100,20,300,20,300,10,200,20,500,10,100,100,0])
            owner.FogMachine.Fire([0,14000,2000])
        def Execute(cls, owner):

            if owner.ResetButton.Pressed():
                owner.FSM.changeState(QuickScare())

        def Exit(cls, owner):
            print("Exiting Intro")
            owner.StartButton.Disable()
            owner.ResetButton.Disable()
            #owner.FSM.setGlobalState(Empty())

        def OnMessage(cls,owner):
            return False


class QuickScare(object):
    __prevClockTime = 0

    def Name(cls):
        return "QUICKSCARE"

    def Enter(cls, owner):
        print("enter QuickScare")
        #owner.StartButton.Enable()
        #owner.ResetButton.Enable()
        owner.MessageManager.sendScare()
        owner.Lights.Fire([4000])
        owner.FogMachine.Reset()
        owner.FogMachine.Fire([2000])

    def Execute(cls, owner):
        #Execute Scare here
        #Flicker Lights
        #Execute Fogger
        #return to Lighting
        if not owner.Lights.isFiring():
            owner.FSM.changeState(Waiting())


    def Exit(cls, owner):
        print("Exiting Quickscare")
        #owner.StartButton.Disable()
        #owner.ResetButton.Disable()
        #owner.FSM.setGlobalState(Empty())

    def OnMessage(cls, owner):
        return False


class Quit(object):

        def Name(cls):
            return "LOSER"

        def Enter(cls, owner):
            print("enter Quit")

            owner.Screen.clearScreen()


        def Execute(cls, owner):
            print("Executing quit")

        def Exit(cls, owner):
            print("Exiting qyut")

        def OnMessage(cls, owner):
            return False

