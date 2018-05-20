import time
import win32serviceutil
import win32service
import win32event
import servicemanager


class CitestService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CitestService"
    _svc_display_name_ = "Citest Service"


    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        self.counter = 0

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
							  servicemanager.PYS_SERVICE_STARTED,
							  (self._svc_name_, ''))
        self.main()

    def log(self, msg):
	    servicemanager.LogInfoMsg(msg)

    def inc_counter(self):
        self.log('Citest Counter: %s' % self.counter)
        self.counter = self.counter + 1


    def main():
	    while self.running == True:
             self.inc_counter()

if __name__ == '__main__':
	win32serviceutil.HandleCommandLine(CitestService)
