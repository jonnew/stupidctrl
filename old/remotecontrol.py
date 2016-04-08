from recordaction import RecordAction
import threading
import zmq

class RemoteControl(threading.Thread):

    def __init__(self, ctx, host, rec_ctl):
        threading.Thread.__init__(self)
        self.socket = ctx.socket(zmq.REP)
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        self.socket.bind(host)
        self.rec_ctl = rec_ctl
        self.stop = threading.Event()

    def run(self):
        print('I: Starting remote controller on thread ' + self.getName())

        while True and not self.stopped():
            socks = dict(self.poller.poll(100))
            if socks.get(self.socket) == zmq.POLLIN:
                cmd = self.socket.recv().decode('ascii')
                action = RecordAction(cmd)
                response = self.rec_ctl.run(action)
                self.socket.send_string(response)
                if action.action == 'quit':
                    break

        print('I: Stopping remote controller on thread ' + self.getName())

    def quit(self):
        self.stop.set()

    def stopped(self):
        return self.stop.isSet()
