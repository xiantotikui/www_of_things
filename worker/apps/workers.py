import time
import os

import zc.lockfile

from .models import *

class Workers:
    def __init__(self, name, secounds):
        self.name = name
        self.secounds = secounds

    def worker(self):
        try:
            lock = zc.lockfile.LockFile('lock')
            try:
                worker = Worker.objects.get(worker_name=self.name)
                WorkerState.objects.create(worker_device=worker, worker_state='on')
                t_end = time.time() + self.secounds
                while time.time() < t_end:
                    time.sleep(1)
                    print('state: on')
                print('state: off')
                WorkerState.objects.create(worker_device=worker, worker_state='off')
            except:
                pass
        except:
            pass
        try:
            lock.close()
        except:
            pass

        return
