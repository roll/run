from subprocess import Popen, PIPE
from .task import Task

class SubprocessTask(Task):

    #Public

    def __init__(self, prefix=''):
        self._prefix = prefix
        
    def invoke(self, command):
        ecommand = self._prefix+command
        process = Popen(ecommand, shell=True, 
            stdin=PIPE, stdout=PIPE, stderr=PIPE)
        returncode = process.wait()
        if returncode != 0:
            raise RuntimeError(
                'Command "{ecommand}" exited with "{returncode}"'.
                format(ecommand=ecommand, returncode=returncode))