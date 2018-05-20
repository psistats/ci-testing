import sys
import time
import win32serviceutil
import win32service
import win32event
import win32timezone
import servicemanager
import socket
from citest.win_business import WinBusiness

class CitestService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CitestService"
    _svc_display_name_ = "Citest Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self._running = False
        self.counter = 0


    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

        win32event.SetEvent(self.hWaitStop)
        self._running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self._running = True
        self.main()

    def log(self, msg):
        servicemanager.LogInfoMsg(msg)

    def counter(self):
        self.log('Citest Counter: %s' % self.counter)
        self.counter = self.counter + 1
        time.sleep(1)

    def main(self):

        self.b = WinBusiness()

        while self._running == True:
            self.log('Citest Counter: %s' % self.b.counter)
            self.b.run()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(CitestService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(CitestService)
