try:
    import tkinter as tk
    import tkinter.font as tkf
except:
    import Tkinter as tk
    import tkFont as tkf

from connectionbar import ConnectionBar
from filenamebar import FileNameBar

class GUI(tk.Frame):

    ##
    # @brief A local UI that distributes control signals to remote control
    # interfaces. There is no state-based logic here! All logic is determined
    # through interaction with a state machine that is used to update the UI's
    # enabled controls.
    #
    # @param parent
    # @param devices Remote control devices to talk with
    #
    # @return
    def __init__(self, parent, devices, sm):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.font = parent.font

        # Common file name
        self.filename = FileNameBar(self)

        # The remote interfaces we are interested in controlling
        self.connections = [ConnectionBar(self, dev) for dev in devices]

        # Recording control rec_btns
        self.rec_btns = {}

        # State machine that drives GUI logic and repaint
        self.sm = sm

        self.initUI()

    def initUI(self):

        self.config(borderwidth=2, relief=tk.RAISED)
        self.pack()

        # Current row counter
        i = 0

        # Common file name to issue during call to 'rename'. Empty means use the
        # same one that the remote recorder already was using.
        l_filename = tk.Label(self, text='Common File Name', font=self.font)
        l_filename.grid(row=i, column=0)
        i+=1

        self.filename.grid(row=i, column=0, pady=5, sticky='ew')
        i+=1

        # Connection UIs
        l_endpoints = tk.Label(self, text='Remote Endpoints', font=self.font)
        l_endpoints.grid(row=i, column=0)
        i+=1

        # Align the Remote Connection components
        start_row = i
        for j,c in enumerate(self.connections):
            i = start_row + j
            c.grid(row=i, column=0, pady=5, sticky='ew')
        i += 1

        b_frame = tk.Frame(self)

        # Record control rec_btns
        l_controls = tk.Label(self, text='Remote Controls', font=self.font)
        l_controls.grid(row=i, column=0)
        i += 1

        # Only events that I defined with triggers for state transitions,
        # rather than those implicitly generated because of callbacks
        ev = {k: v for k, v in self.sm.events.items() if not k.startswith('to_')}
        for t in sorted(ev.keys()):

            #trig = getattr(self.sm, ev[t].name)
            #def cb():
            #    trig()
            #    self.paint()

            self.rec_btns[t] = tk.Button(b_frame, text=t, state='disabled', font=self.font,
                    command=getattr(self.sm, ev[t].name))
            self.rec_btns[t].pack(side='left', fill=None, expand=False, padx=10)

            b_frame.grid(row=i, column=0, sticky="w", padx=10)

        self.paint()

    def paint(self):

        # Get current  state
        state_curr = self.sm.current_state.name
        print('Current state: ' + state_curr)
    
        # Disable all buttons 
        for k, v in self.rec_btns.items():
            v['state'] = 'disabled'

        # Enable those buttons defining valid triggers for current state
        ev = {k: v for k, v in self.sm.events.items() if not k.startswith('to_')}
        for k, v in ev.items():
            for k in v.transitions[state_curr]:
                self.rec_btns[v.name]['state'] = 'normal'
                print(v.name)
