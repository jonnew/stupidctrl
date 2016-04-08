# Implement record control state machine using 'if' statements.
# Not very scalable, but good enough

import string
from recorder import Recorder
from recordstate import RecordState
from recordmachine import RecordMachine
from recordaction import RecordAction

# A different subclass for each RecordState

class Disconnected(RecordState):
    def run(self):
        return 'I: Disconnected from remote recorders.'

    def next(self, input):
        if input == RecordAction.connect:
            return RecordController.waiting
        return RecordController.disconnected

class Connected(RecordState):
    def run(self):
        return 'I: Connected to remote recorders.'

    def next(self, input):
        if input == RecordAction.new:
            return RecordController.file_created
        if input == RecordAction.disconnect:
            return RecordController.disconnected
        return RecordController.connected

class FileCreated(RecordState):
    def run(self):
        RecordController.recorder.open_file() 
        return 'I: New file created.'

    def next(self, input):
        if input == RecordAction.start:
            return RecordController.recording
        if input == RecordAction.disconnect:
            return RecordController.disconnected
        return RecordController.file_created

class Recording(RecordState):
    def run(self):
        RecordController.recorder.start()
        return 'I: Recording started.'

    def next(self, input):
        if input == RecordAction.pause:
            return RecordController.paused
        return RecordController.recording

class Paused(RecordState):
    def run(self):
        RecordController.recorder.pause()
        return 'I: Recording paused.'

    def next(self, input):
        if input == RecordAction.start:
            return RecordController.recording
        if input == RecordAction.new:
            return RecordController.file_created
        if input == RecordAction.disconnect:
            return RecordController.disconnected
        return RecordController.paused

class RecordController(RecordMachine):
    def __init__(self, recorder):
        # Handle of recorder to be controlled
        RecordController.recorder = recorder; 
        # Initial state
        RecordMachine.__init__(self, RecordController.waiting)

# Static variable init
RecordController.disconnected = Disconnected()
RecordController.connected = Connected()
RecordController.file_created = FileCreated()
RecordController.recording = Recording()
RecordController.paused = Paused()
RecordController.quitting = Quitting()
