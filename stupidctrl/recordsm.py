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
            State(name='disconnected',  on_enter=['updateUI']),
            State(name='connected',     on_enter=['updateUI']),
            State(name='confirmed',     on_enter=['updateUI']),
            State(name='ready',         on_enter=['updateUI', 'prepRecording']),
            State(name='started',       on_enter=['updateUI', 'startRecording']),
            State(name='paused',        on_enter=['updateUI', 'pauseRecording'])
        ]

        # Record controller state transition definition
        transitions = [
            {'trigger': 'connect',    'source': 'disconnected', 'dest': 'connected'    , 'prepare': ['connectToServers', 'pingServers'], 'conditions': 'connection_confirmed'},
            #{'trigger': 'ping',       'source': 'connected',    'dest': 'confirmed'    , 'prepare': 'pingServers', 'conditions': 'connection_confirmed'}, 
            {'trigger': 'disconnect', 'source': 'connected',    'dest': 'disconnected' },
            #{'trigger': 'disconnect', 'source': 'confirmed',    'dest': 'disconnected' },
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

    # TODO: This circular composition feels very icky. It would be best just
    # to have a gui.paint() triggered after any click event within the GUI
    # code.
    def set_gui(self, gui):
        self.gui = gui

    def updateUI(self):
        if self.gui:
            self.gui.paint()

    def connectToServers(self):
        print("Connecting to servers.")
        self.manifold.filterRemotes()
        self.manifold.connect()

    def connection_confirmed(self): 
        return self.manifold.connection_confirmed

    def pingServers(self):
        print("Testing connections.")
        self.manifold.ping()
        print("Connection confirmed: " + str(self.connection_confirmed()))

    def prepRecording(self):
        print("Preparing recording.")
        self.manifold.makeNewFile()

    def startRecording(self):
        print("Starting recording.")
        self.manifold.sendStart()

    def pauseRecording(self):
        print("Pausing")
        self.manifold.sendPause()
