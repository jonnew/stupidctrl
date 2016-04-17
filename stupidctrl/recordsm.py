from transitions import Machine, State
from remote import ControlManifold

# TODO: Should be singleton
class RecordSM(Machine):

    ##
    # @brief A record controller state machine.
    #
    # @param List of remote interfaces to control
    #
    # @return void
    def __init__(self, manifold):
        self.manifold = manifold
        self.gui = None

        # Record controller states
        states = [
            State(name='disconnected',  on_enter=['update_ui']),
            State(name='connected',     on_enter=['update_ui', 'connect_to_servers']),
            State(name='ready',         on_enter=['update_ui', 'prep_recording']),
            State(name='started',       on_enter=['update_ui', 'start_recording']),
            State(name='paused',        on_enter=['update_ui', 'pause_recording'])
        ]

        # Record controller state transition definition
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

    # TODO: This circular componsition feels very icky. It would be best just
    # to have a gui.paint() triggered after any click event within the GUI
    # code.
    def set_gui(self, gui):
        self.gui = gui

    def update_ui(self):
        if self.gui:
            print("Updating UI")
            self.gui.paint()

    def connect_to_servers(self):
        print("Connecting to servers.")
        self.manifold.connect()
        #pass
        #rec_ctrl.test_connection()

    def test_connection(self):
        print("Testing connection.")
        #pass
        #rec_ctrl.test_connection()

    def prep_recording(self):
        print("Preping recording.")
        self.manifold.makeNewFile()

    def start_recording(self):
        print("Starting recording.")
        self.manifold.sendStart()

    def pause_recording(self):
        print("Pausing")
        self.manifold.sendPause()
