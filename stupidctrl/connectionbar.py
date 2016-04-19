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

        # The requested address.
        # No verificaction of sanity at this point
        self.req_addr = remote.req_addr
        self.name = remote.name

        # Is this connection active?
        self.active = tk.IntVar()

        self.initUI()

    def initUI(self):

        # Grid config
        self.columnconfigure(1, weight=1)

        # Label
        label = tk.Label(self, font=self.font, text=self.name, width=15, anchor=tk.W)
        label.grid(row=0, column=0, padx=10, sticky=tk.W)

        # Text entry
        entry = tk.Entry(self, font=self.font)
        entry.delete(0, tk.END)
        entry.insert(0, self.req_addr)
        entry.grid(row=0, column=1, sticky=tk.W+tk.E)
        entry.bind('<Leave>', lambda event: self.updateAddr(event))

        cbox = tk.Checkbutton(self, text="Active", variable=active)
        cbox.grid(row=0, column=2, sticky=tk.E)

    # Udpate socket address
    def updateAddr(self, event):

        txt = event.widget.get()
        if txt:
            self.req_addr = txt
        else:
            self.req_addr = None

