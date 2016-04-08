#!/usr/bin/python

'''
A stupid GUI to control oat-record and some other crap remotely.

Warning: I don't know how to write Python.
'''

try:
    import tkinter as tk
    import tkinter.font as tkf
except:
    import Tkinter as tk
    import tkFont as tkf

from recordingpanel import RecordingPanel
from filenamebar import FileNameBar
from recordsm import RecordSM 
import zmq
import signal
import sys

# Exit routine
def signal_handler(signal, frame):
    print('Exiting')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Generic remote connction for interacting with a single device
class RemoteConnectionBar(tk.Frame):

    def __init__(self, parent, device):

        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.font = parent.font

        # RecordingPanel reference
        self.device = device

        self.initUI()

    def initUI(self):

        # Grid config
        self.columnconfigure(1, weight=1)

        # Label
        label = tk.Label(self, font=self.font, text=self.device.name, width=15, anchor=tk.W)
        label.grid(row=0, column=0, padx=10, sticky=tk.W)

        # Text entry
        entry = tk.Entry(self, font=self.font)
        entry.delete(0, tk.END)
        entry.insert(0, self.device.req_addr)
        entry.grid(row=0, column=1, sticky=tk.W+tk.E)
        entry.bind('<Leave>', lambda event: self.updateEndpoint(event))

        # Connect button
        b_conn_txt = tk.StringVar()
        b_conn_txt.set('Connect')
        b_conn = tk.Button(self, textvariable=b_conn_txt, font=self.font, width=15,
                command = lambda: self.connect(b_conn_txt, label))
        b_conn.grid(row=0, column=2, padx=10, sticky=tk.E)

    # Connect/Disconnect from remote endpoint
    def connect(self, txt, label):
        if not self.device.is_connected:
            try:
                self.device.connect()
            except zmq.ZMQError:
                self.device.conn_addr = None
                print ('Failed: Invalid ' + self.device.name + ' endpoint.')
                return

            self.device.conn_addr = self.device.req_addr
            label.config(fg='green')
            txt.set('Disconnect')
        else:
            try:
                self.device.disconnect()
            except zmq.ZMQError:
                print ('Failed to disconnected from ' + self.device.name + ' endpoint.')

            label.config(fg='black')
            txt.set('Connect')

    # Udpate socket address
    def updateEndpoint(self, event):

        txt = event.widget.get()
        if txt:
            self.device.req_addr = txt
        else:
            self.device.req_addr = None

# Basic GUI
class RecordControlBar(tk.Frame):

    def __init__(self, parent, devices):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.font = parent.font

        # Common file name
        self.filename = FileNameBar(self)

        # The devices we are interested in contolling
        self.connections = [RemoteConnectionBar(self, dev) for dev in devices]

        self.initUI()

    def initUI(self):

        self.config(borderwidth=2, relief=tk.RAISED)
        self.pack()

        # Current row counter
        i = 0

        # Common file name to issue during call to 'new'. Empty means use the
        # same one that the remot recorder already was using.
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

        # Record control buttons
        l_controls = tk.Label(self, text='Remote Controls', font=self.font)
        l_controls.grid(row=i, column=0)
        i+=1

        b_help = tk.Button(b_frame, text='Help', state='disabled', font=self.font, command=self.printHelp)
        b_start = tk.Button(b_frame, text='Start', state='disabled', font=self.font, command=self.startRecording)
        b_stop = tk.Button(b_frame, text='Stop', state='disabled', font=self.font, command=self.stopRecording)
        b_new = tk.Button(b_frame, text='New', state='disabled', font=self.font, command=self.makeNewFile)
        b_exit = tk.Button(b_frame, text='Quit', state='disabled', font=self.font, command=self.quitAll)

        b_help.pack(side='left', fill=None, expand=False, padx=10)
        b_start.pack(side='left', fill=None, expand=False, padx=10)
        b_stop.pack(side='left', fill=None, expand=False, padx=10)
        b_new.pack(side='left', fill=None, expand=False,  padx=10)
        b_exit.pack(side='left', fill=None, expand=False, padx=10)

        b_frame.grid(row=i, column=0, sticky="w", padx=10)

    def printHelp(self):
        for i, conn in enumerate(self.connections):
            if conn.device.is_connected:
                conn.device.getHelp()

    def startRecording(self):
        for i, conn in enumerate(self.connections):
            if conn.device.is_connected:
                conn.device.sendStart()

    def stopRecording(self):
        for i, conn in enumerate(self.connections):
            if conn.device.is_connected:
                conn.device.sendStop()

    def makeNewFile(self):
        for i, conn in enumerate(self.connections):
            if conn.device.is_connected:
                conn.device.makeNewFile()

    def quitAll(self):
        for i, conn in enumerate(self.connections):
            if conn.device.is_connected:
                conn.device.sendQuit()

def update_ui(state):
    pass    

def main():

    devices = [ RecordingPanel('Open Ephys', 'tcp://localhost:5556', '', 'StartRecord', 'StopRecord', 'NewFile',''),
                RecordingPanel('Oat', 'tcp://localhost:6666', 'help\n', 'start\n', 'pause\n', 'new\n', 'quit\n'),
                RecordingPanel('Maze', 'tcp://localhost:6665', 'help', 'start', 'pause', 'new', 'exit'),
                RecordingPanel('Stim', 'tcp://localhost:6000', '', 'start', 'pause', 'new', 'quit')
              ] 

    root = tk.Tk()
    root.title('Stupid Controller')
    root.font = tkf.Font(family='Helvetica', size=12)
    app = RecordControlBar(root, devices)
    root.mainloop()

if __name__ == '__main__':
    main()
