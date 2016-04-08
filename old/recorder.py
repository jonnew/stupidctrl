import datetime
import json
import os

class Recorder:

    def __init__(self, folder, name):
        self.folder = folder
        self.name = name
        self.paused = True
        self.f = None

    def open_file(self):
        date = datetime.datetime.now()
        fid = date.strftime(self.folder + '%Y-%m-%d-%H-%M-%S') + \
            '_' + self.name + '.json'
        self.f = open(fid, 'wb')
        self.f.write(bytes('{', 'utf8'))

    def close_file(self):
        if self.f != None:
            self.f.seek(-1, os.SEEK_END)
            self.f.truncate()
            self.f.write(bytes('}', 'utf8'))

    def pause(self):
        self.paused = True

    def start(self):
        self.paused = False

    def write(self, tick, datum):
        if not self.paused:
            dat = '\"' + str(tick) + '\":'
            dat += json.dumps(datum)
            dat += ','
            self.f.write(bytes(dat, 'utf8'))
