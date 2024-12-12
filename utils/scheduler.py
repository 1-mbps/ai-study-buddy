'''Function thread schedulings
'''

import threading

class FunctionScheduler:
    '''Schedule a fuction call
    '''
    def __init__(self):
        self._timer = None

    def schedule_function(self, interval, function, *args, **kwargs):
        """
        Schedule a function to run in [interval] seconds.
        """
        if self._timer is not None:
            self.cancel()
        self._timer = threading.Timer(interval, function, args=args, kwargs=kwargs)
        self._timer.start()

    def cancel(self):
        '''Cancel scheduled call'''
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None