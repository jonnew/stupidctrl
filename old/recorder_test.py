from recorder import Recorder

r = Recorder()

r.open_file('./', 'lala')

a = {'lala':2}

r.write(a)

#recorder.close_file()
