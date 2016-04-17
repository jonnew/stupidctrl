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

from remote import RemoteInterface, ControlManifold
from gui import GUI
from recordsm import RecordSM
import signal
import sys

# Exit routine
def signal_handler(signal, frame):
    print('Exiting')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():

    # Define a set of interfaces to control
    remotes = [
        RemoteInterface('Open Ephys', 'tcp://localhost:5556', '', 'StartRecord', 'StopRecord', 'NewFile',''),
        RemoteInterface('Oat', 'tcp://localhost:6666', 'help\n', 'start\n', 'pause\n', 'new\n', 'quit\n'),
        RemoteInterface('Maze', 'tcp://localhost:6665', 'help', 'start', 'pause', 'new', 'exit'),
        RemoteInterface('Stim', 'tcp://localhost:6000', '', 'start', 'pause', 'new', 'quit')
    ]
    
    # Wrap remote interfaces
    manifold = ControlManifold(remotes)

    # Pass to state machine to provide control logic
    sm = RecordSM(manifold)

    root = tk.Tk()
    root.title('Stupid Controller')
    root.font = tkf.Font(family='Helvetica', size=12)
    gui = GUI(root, remotes, sm)
    sm.set_gui(gui)
    root.mainloop()

if __name__ == '__main__':
    main()
