import os

class Business():

    def __init__(self):
        self.counter = 0

    def run(self, amt=None):
        if amt == None:
            amt = 1

        if os.name == 'nt':
            amt = amt + 1

        self.counter = self.counter + amt

