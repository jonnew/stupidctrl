from transitions import Machine, State

# TODO: Should be singleton
class RecordSM(Machine):

    ## 
    # @brief A record controller state machine.
    # 
    # @param recorder Recorder to control
    # @param ui GUI to update in corespondance with current state.
    # 
    # @return void
    def __init__(self, recorder, ui):
        self.recorder = recorder
        self.ui = ui

        # Record controller states
        states = [
            State(name='disconnected', on_enter=['update_ui']),
            State(name='connected',  on_enter=['update_ui', 'test_connection']),
            State(name='ready', on_enter=['update_ui', 'prep_recording']),
            State(name='started', on_enter=['update_ui', 'start_recording']),
            State(name='paused', on_enter=['update_ui', 'pause_recording'])
        ]

        # Record controller state transition defintion
        transitions = [
            {'trigger': 'connect',    'source': 'disconnected', 'dest': 'connected'    },
            {'trigger': 'disconnect', 'source': 'connected',    'dest': 'disconnected' },
            {'trigger': 'disconnect', 'source': 'paused',       'dest': 'disconnected' },
            {'trigger': 'new',        'source': 'connected',    'dest': 'ready'        },
            {'trigger': 'new',        'source': 'paused',       'dest': 'ready'        },
            {'trigger': 'start',      'source': 'ready',        'dest': 'started'      },
            {'trigger': 'pause',      'source': 'started',      'dest': 'paused'       },
        ]

        # Record machine
        Machine.__init__(self,
                         states=states,
                         transitions=transitions,
                         initial='disconnected')

    def update_ui(self):
        ui.update(self.state)

    def test_connection(self):
        pass
        #recorder.test_connection()

    def prep_recording(self):
        recorder.open_file()

    def start_recording(self):
        recorder.start()

    def pause_recording(self):
        recorder.pause()
