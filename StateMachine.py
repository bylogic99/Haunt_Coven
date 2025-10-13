
class StateMachine:
    def __init__(self, owner, initialState):
        self.__owner = owner

        self.__currentState = initialState
        self.__prevState = None
        self.__globalState = None

    def changeState(self, newState):

        self.__prevState = self.__currentState

        if self.__currentState is not None:
            self.__currentState.Exit(self.__owner)

        self.__currentState = newState

        self.__currentState.Enter(self.__owner)

    def setGlobalState(self, state):
        self.__globalState = state

    def update(self):
        if self.__globalState is not None:
            self.__globalState.Execute(self.__owner)

        if self.__currentState is not None:
            self.__currentState.Execute(self.__owner)

    def revertToPreviousState(self):
        self.changestate(self.__prevState)

    def isInState(self, state):
        return state.Name() == self.__currentState.Name()

    def prevStateName(self):
        return self.__prevState.Name()


    def handleMessage(self, msg):
        self.__owner.Message = msg
        if self.__currentState is not None and self.__currentState.OnMessage(self.__owner):
            self.__owner.Message = ""
            return True

        if self.__globalState is not None and self.__globalState.OnMessage(self.__owner):
            self.__owner.Message = ""
            return True

        return False