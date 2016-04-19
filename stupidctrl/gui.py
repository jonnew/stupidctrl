try:
    import tkinter as tk
    import tkinter.font as tkf
except:
    import Tkinter as tk
    import tkFont as tkf

class ConnectionBar(tk.Frame):

    ##
    # @brief
    #
    # @param parent
    # @param default_addr
    #
    # @return
    def __init__(self, parent, remote):

        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.font = parent.font

        # Remote controller bound to this GUI
        self.remote = remote

        # The requested address.
        # No verificaction of sanity at this point
        self.name = remote.name

        # Is this connection active?
        self.active = tk.IntVar()
        
        # Text entry bar and checkbox
        self.entry = None
        self.cbox = None

        self.initUI()

    def initUI(self):

        # Grid config
        self.columnconfigure(1, weight=1)

        # Label
        label = tk.Label(self, font=self.font, text=self.name, width=15, anchor=tk.W)
        label.grid(row=0, column=0, padx=10, sticky=tk.W)

        # Text entry
        self.entry = tk.Entry(self, font=self.font)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.remote.req_addr)
        self.entry.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.entry.bind('<Leave>', lambda event: self.updateAddr(event))

        self.cbox = tk.Checkbutton(self, text="Active", variable=self.active, command=self.toggleActive)
        self.cbox.grid(row=0, column=2, sticky=tk.E)

    def updateAddr(self, event):

        txt = event.widget.get()
        if txt:
            self.remote.req_addr = txt
        else:
            self.remote.req_addr = None

    def toggleActive(self):

        if self.active.get():
            self.remote.is_active = True
        else :
            self.remote.is_active = False

    def disable(self):
       self.cbox['state'] = 'disable'
       self.entry['state'] = 'disable'

    def enable(self):
       self.cbox['state'] = 'normal'
       self.entry['state'] = 'normal'

class FileNameBar(tk.Frame):

    ## 
    # @brief A file name entry bar.
    # 
    # @param parent Frame to place bar within.
    # 
    # @return 
    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.font = parent.font
        self.filename = None
        self.initUI()

    def initUI(self):

        # Grid config
        self.columnconfigure(1, weight=1)

        # Label
        label = tk.Label(self, font=self.font, text='File name', width=15,
                anchor=tk.W)
        label.grid(row=0, column=0, padx=10, sticky=tk.W)

        # Text entry
        entry = tk.Entry(self, font=self.font)
        entry.delete(0, tk.END)
        entry.insert(0, 'file')
        entry.grid(row=0, column=1, sticky=tk.W+tk.E)
        entry.bind('<Leave>', lambda event: self.updateFileName(event))

    # Udpate socket address
    def updateFileName(self, event):

        txt = event.widget.get()
        if txt:
            self.filename = txt
        else:
            self.filename = None

class GUI(tk.Frame):

    ##
    # @brief A local UI that distributes control signals to remote control
    # interfaces. There is no state-based logic here! All logic is determined
    # through interaction with a state machine that is used to update the UI's
    # enabled controls.
    #
    # @param parent
    # @param remotes Remote control remotes to talk with
    #
    # @return
    def __init__(self, parent, remotes, sm):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.font = parent.font

        # Common file name
        self.filename = FileNameBar(self)

        # The remote interfaces we are interested in controlling
        self.connections = [ConnectionBar(self, r) for r in remotes]

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

        # If we are in any state but disconnected, user should not be able to
        # change remote addr/active states
        if state_curr is 'disconnected':
            for c in self.connections:
                c.enable()
        else:
            for c in self.connections:
                c.disable()

