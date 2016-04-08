# Record control state machine

class RecordMachine:

    def __init__(self, initialState):
        self.currentState = initialState
        self.currentState.run()

    # Template method:
    def run(self, cmd):
        self.currentState = self.currentState.next(cmd)
        return self.currentState.run()
