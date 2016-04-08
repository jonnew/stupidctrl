# Record control input action

class RecordAction:
    def __init__(self, action):
        self.action = action
    def __str__(self):
        return self.action
    def __eq__(self, other):
        return self.action == other.action
    def __hash__(self):
        return hash(self.action)

# Static possible record actions
RecordAction.connect = RecordAction('connect')
RecordAction.disconnect = RecordAction('disconnect')
RecordAction.start = RecordAction('start')
RecordAction.pause = RecordAction('pause')
RecordAction.new = RecordAction('new')
