try:
    import tkinter as tk
    import tkinter.font as tkf
except:
    import Tkinter as tk
    import tkFont as tkf

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
