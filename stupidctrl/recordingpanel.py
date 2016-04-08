import collections
import zmq 

# RPC command set
RPCInterface = collections.namedtuple('RPC', ['socket', 'poll'])

## 
# @brief Generic control panel of a remote recording interface. A recording panel must
# implement the following methods:
# - start       start recording
# - pause       pause previously started recording
# - new         start new recording without changing the base file name
# - rename ARG  start a new recording with a base file name specified by ARG
# - quit        close remote control connection and return to normal state
class RecordingPanel(object):

    def __init__(self, name, addr, help_cmd="help", start_cmd="start",
            pause_cmd="pause", newfile_cmd="new", quit_cmd="quit"):

        self.ctx = zmq.Context()
        self.name = name
        self.is_connected = False
        self.help_cmd = help_cmd
        self.start_cmd = start_cmd
        self.pause_cmd = pause_cmd
        self.newfile_cmd = newfile_cmd
        self.quit_cmd = quit_cmd
        self.req_addr = addr
        self.conn_addr = None
        self.retries = 3
        self.retries_left = self.retries
        self.request_timeout = 100 # msec

    def __enter__(self):
        return self

    def connect(self):
        self.rpc = RPCInterface(self.ctx.socket(zmq.REQ), zmq.Poller())
        self.rpc.socket.connect(self.req_addr)
        self.rpc.poll.register(self.rpc.socket, zmq.POLLIN)
        self.is_connected = True

    def disconnect(self):
        self.rpc.socket.setsockopt(zmq.LINGER, 0)
        self.rpc.socket.close()
        self.rpc.poll.unregister(self.rpc.socket)
        self.is_connected = False

    ## 
    # @brief Send RPC to remote recording controller. This procedure implements
    # the 'lazy pirate' pattern to prevent infinite blocks in case of remote
    # server crash etc.
    # 
    # @param request Requested action @return True a response is received to
    # the request. False if communication times out.
    def sendMsg(self, request):
        
        print("I [%s]: Sending \'%s\'\n" % (self.name, request.rstrip()))
        self.rpc.socket.send_string(str(request))

        while True:
            socks = dict(self.rpc.poll.poll(self.request_timeout))
            if socks.get(self.rpc.socket) == zmq.POLLIN:
                reply = self.rpc.socket.recv()
                if not reply:
                    break
                else:
                    print("I [%s]: Received: %s" % (self.name, reply))
                    self.retries_left = self.retries
                    return True # Success
            else:
                print("W [%s]: No response from server, retrying...", self.name)
                # REQ/REP socket is in confused state. Close it and create another.
                self.disconnect()
                self.retries_left -= 1
                self.connect()

                if self.retries_left == 0:
                    self.retries_left = self.retries
                    print("E: [%s] Server offline, abondoning." % self.name)
                    break

                # If we have not exhausted retries, try again
                print("I [%s]: Reconnecting and resending (%s)" % (self.name, request))
                self.rpc.socket.send_string(str(request))

        return False # Failure

    def getHelp(self):
        if self.help_cmd:
            self.sendMsg(self.help_cmd)

    def sendStart(self):
        if self.start_cmd:
            self.sendMsg(self.start_cmd)

    def sendStop(self):
        if self.pause_cmd:
            self.sendMsg(self.pause_cmd)

    def makeNewFile(self):
        if self.newfile_cmd:
            self.sendMsg(self.newfile_cmd)

    def makeNamedNewFile(self):
        if self.namednewfile_cmd:
            self.sendMsg(self.namednewfile_cmd)

    def sendQuit(self):
        if self.quit_cmd:
            self.sendMsg(self.quit_cmd)
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.is_connected:
            self.disconnect()
        self.ctx.term()

