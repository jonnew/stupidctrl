from transitions import Machine, State
from .remote import ControlManifold

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
            State(name='disconnected',  on_enter=['unbusyUI', 'updateUI']),
            State(name='connected',     on_enter=['unbusyUI', 'updateUI']),
            State(name='confirmed',     on_enter=['unbusyUI', 'updateUI']),
            State(name='ready',         on_enter=['unbusyUI', 'updateUI', 'prepRecording']),
            State(name='started',       on_enter=['unbusyUI', 'updateUI', 'startRecording']),
            State(name='paused',        on_enter=['unbusyUI', 'updateUI', 'pauseRecording'])
        ]

        # Record controller state transition definition
        transitions = [
            {'trigger': 'connect',    'source': 'disconnected', 'dest': 'connected'    , 'prepare': ['busyUI', 'connectToServers', 'pingServers'], 'conditions': 'connection_confirmed'},
            {'trigger': 'disconnect', 'source': 'connected',    'dest': 'disconnected' , 'prepare': ['busyUI'] },
            {'trigger': 'disconnect', 'source': 'paused',       'dest': 'disconnected' , 'prepare': ['busyUI'] },
            {'trigger': 'new',        'source': 'connected',    'dest': 'ready'        , 'prepare': ['busyUI'] },
            {'trigger': 'new',        'source': 'paused',       'dest': 'ready'        , 'prepare': ['busyUI'] },
            {'trigger': 'start',      'source': 'ready',        'dest': 'started'      , 'prepare': ['busyUI'] },
            {'trigger': 'pause',      'source': 'started',      'dest': 'paused'       , 'prepare': ['busyUI'] },
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

    def busyUI(self):
        if self.gui:
            self.gui.busy()

    def unbusyUI(self):
        if self.gui:
            self.gui.unbusy()

    def connectToServers(self):
        print("Connecting to servers.")
        self.manifold.filterRemotes()
        self.manifold.connect()

    def connection_confirmed(self): 
        self.unbusyUI()
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
